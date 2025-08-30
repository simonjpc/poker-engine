from flask import Flask, jsonify, request
from flask_cors import CORS
from game import Game
from assistant import  determine_position, classify_hand, determine_action, get_updated_ranges
from flop_assistant import recommend_action
import threading

app = Flask(__name__)
CORS(app, supports_credentials=True)

game_instance = None
config_locked = False

@app.route('/game_state', methods=['GET'])
def get_game_state():
    """
    Get the current game state, including players, stacks, and community cards.
    """
    active_player_name = None
    game_state = {}
    if game_instance is not None:
        if game_instance.current_betting_round:
            active_player_name = game_instance.current_betting_round.get_active_player()
        if game_instance is not None:
            game_state = {
                "players": [
                    {
                        "name": p.name,
                        "stack": p.stack,
                        "hole_cards": p.hole_cards if p.name.lower() == "you" else ["🂠", "🂠"],
                        "folded": p.folded,
                        "all_in": p.all_in,
                        "current_bet": p.current_bet,
                        "selectedHoleCards": p.selected_hole_cards,
                    } for p in game_instance.players
                ],
                "community_cards": game_instance.community_cards,
                "pot": game_instance.pot,
                "current_hand": game_instance.hand_number,
                "dealer_position": game_instance.dealer_position,
                "active_player": active_player_name,
                "awaiting_flop_input": game_instance.awaiting_flop_input if hasattr(game_instance, "awaiting_flop_input") else False,
                "awaiting_turn_input": game_instance.awaiting_turn_input if hasattr(game_instance, "awaiting_turn_input") else False,
            }
    return jsonify(game_state)

@app.route('/action', methods=['POST'])
def player_action():
    """
    Handle player actions (fold, call, raise).
    """
    data = request.json
    player_name = data.get("player")
    action = data.get("action")
    amount = float(data.get("amount", 0)) # this is only valid for "raise" action
    player = next((p for p in game_instance.players if p.name == player_name), None)
    
    if not player:
        return jsonify({"error": "Player not found"}), 404

    valid_actions = game_instance.current_betting_round.get_valid_actions(player)

    if action not in valid_actions:
        return jsonify({"error": "Invalid action for this player"}), 400

    if action == "call":
        amount = valid_actions[action]
    player.pending_action = (action, amount)

    return jsonify({"message": f"{player_name} {action}ed"})

@app.route('/next_hand', methods=['POST'])
def next_hand():
    """
    Start the next hand.
    """
    game_instance.play_hand()
    return jsonify({"message": "Next hand started"})

@app.route('/game_config', methods=['POST'])
def configure_game():
    
    global game_instance, config_locked

    if config_locked:
        return jsonify({"error": "Game already started"}), 403

    data = request.get_json()
    players_config = data.get("players", [])
    button_index = data.get("button_player_index", 0)

    # Filter out unavailable players
    active_players = []
    manual_holecards = {}

    for i, p in enumerate(players_config):
        if p["available"]:
            active_players.append((p["name"], p["amount"]))
            if p.get("selectedHoleCards") and p["name"].lower() == "you":
                manual_holecards["you"] = p["selectedHoleCards"]
    
    dealer_name = players_config[button_index]["name"]
    dealer_index_mapped = ([ap[0] for ap in active_players]).index(dealer_name)

    names = [p[0] for p in active_players]
    stacks = [p[1] for p in active_players]
    game_instance = Game(players=names, starting_stacks=stacks, manual_holecards=manual_holecards)
    print("✅ Game instance created.")
    # game_instance.dealer_position = button_index
    game_instance.dealer_position = dealer_index_mapped

    return jsonify({"message": "Config received"})

@app.route('/start_game', methods=['POST'])
def start_game():
    """
    Start the game.
    """
    global config_locked, game_instance

    if not game_instance:
        print("❌ Cannot start game: game_instance is None")
        return jsonify({"error": "Game not configured"}), 400
    
    config_locked = True

    def run_game():
        game_instance.start_game()
    print("✅ Starting game...")
    threading.Thread(target=run_game).start()
    return jsonify({"message": "Game started"})

@app.route('/recommend_preflop_action', methods=['POST'])
def recommend_preflop_action():
    """
    Recommends an action based on position, hole cards, and betting history.
    Only for the player named "You".
    """
    if not game_instance or not game_instance.current_betting_round:
        return jsonify({"error": "Game not active"}), 400

    player = next((p for p in game_instance.players if p.name.lower() == "you"), None)
    if not player or player.folded or player.all_in:
        return jsonify({"error": "Player not available for recommendation"}), 400

    position_index = (player.position - game_instance.dealer_position) % len(game_instance.players)
    position_name = determine_position(position_index, len(game_instance.players))

    preflop = game_instance.current_betting_round.preflop
    
    hand_code, action, amount = None, None, None
    if len(player.hole_cards):
        hand_code = classify_hand(player.hole_cards)

        has_raiser = any(p.current_bet > game_instance.big_blind for p in game_instance.players if p.name != player.name)

        action, amount = determine_action(
            position=position_name,
            hand=hand_code,
            has_raiser=has_raiser,
            is_first_to_act=not has_raiser,
            num_limpers=sum(1 for p in game_instance.players if p.current_bet == game_instance.big_blind and p.name != player.name),
            bb_value=game_instance.big_blind
        )

    return jsonify({
        "position": position_name,
        "hand": hand_code,
        "recommendation": action,
        "amount": amount,
    })

@app.route('/set_flop', methods=['POST'])
def set_flop():
    if not game_instance or not game_instance.current_betting_round:
        return jsonify({"error": "Game not active"}), 400

    data = request.get_json()
    cards = data.get("flop_cards", [])

    if len(cards) != 3:
        return jsonify({"error": "Flop must have 3 cards"}), 400

    # Prevent duplicate flop if already dealt
    if len(game_instance.community_cards) >= 3:
        return jsonify({"error": "Flop already set"}), 400
    
    # Remove from deck
    game_instance.deck.cards = [c for c in game_instance.deck.cards if c not in cards]
    game_instance.community_cards.extend(cards)
    print(f"✅ Flop set to: {cards}")

    game_instance.awaiting_flop_input = False

    # Proceed with the next betting round
    # game_instance.execute_betting_round("Flop")
    # 🔹 Instead of calling execute_betting_round("Flop") directly:
    import threading
    def start_flop_betting_round():
        game_instance.execute_betting_round("Flop")
        # if game_instance.hand_continues():
        #     game_instance.awaiting_turn_input = True
    threading.Thread(target=start_flop_betting_round, daemon=True).start()

    return jsonify({"message": "Flop set"})

@app.route('/recommend_flop_action', methods=['POST'])
def recommend_flop_action_route():
    """
    Recommends an action based on your hand, the flop, and opponent's range.
    """
    if not game_instance or not game_instance.community_cards or len(game_instance.community_cards) < 3:
        return jsonify({"error": "Flop not dealt yet"}), 400

    player = next((p for p in game_instance.players if p.name.lower() == "you"), None)
    if not player or player.folded or player.all_in:
        return jsonify({"error": "Player not available for recommendation"}), 400

    # Use pre-processed range for now — will be dynamic later
    # For now: assume tight range
    updated_ranges = get_updated_ranges(
        players=game_instance.players,
        big_blind=game_instance.big_blind,
        dealer_position=game_instance.dealer_position,
    )
    game_instance.updated_ranges = updated_ranges
    
    hero_hand = player.hole_cards
    flop = game_instance.community_cards[:3]
    
    opponent_ranges = {
        pos: rng for pos, rng in game_instance.updated_ranges.items()
        if pos != determine_position(
            (player.position - game_instance.dealer_position) % len(game_instance.players),
            len(game_instance.players)
        )
    }

    equity_results = recommend_action(
        hero_hand=hero_hand,
        community=flop,
        updated_opponent_range=opponent_ranges,
        round="flop",
    )   
    print("equity_results: ", equity_results)

    return jsonify({
        "opponent_ranges": opponent_ranges,
        "equity_results": equity_results,
    })

@app.route('/set_turn', methods=['POST'])
def set_turn():
    if not game_instance or not game_instance.current_betting_round:
        return jsonify({"error": "Game not active"}), 400

    data = request.get_json()
    cards = data.get("turn_cards", []) # check where turn cards come from in the frontend

    if len(cards) != 1:
        return jsonify({"error": "Turn must have 4 cards"}), 400

    # Prevent duplicate turn if already dealt
    if len(game_instance.community_cards) >= 4:
        return jsonify({"error": "Turn already set"}), 400
    
    # Remove from deck
    game_instance.deck.cards = [c for c in game_instance.deck.cards if c not in cards]
    game_instance.community_cards.extend(cards)
    print(f"✅ Turn set to: {cards}")

    game_instance.awaiting_turn_input = False # add flag for turn round

    # Proceed with the next betting round
    # game_instance.execute_betting_round("Turn")
    # 🔹 Instead of calling execute_betting_round("Turn") directly:
    import threading
    def start_turn_betting_round():
        game_instance.execute_betting_round("Turn")
    threading.Thread(target=start_turn_betting_round, daemon=True).start()

    return jsonify({"message": "Turn set"})

@app.route('/recommend_turn_action', methods=['POST'])
def recommend_turn_action_route():
    """
    Recommends an action based on your hand, the turn, and opponent's range.
    """
    if not game_instance or not game_instance.community_cards or len(game_instance.community_cards) < 4:
        return jsonify({"error": "Turn not dealt yet"}), 400

    player = next((p for p in game_instance.players if p.name.lower() == "you"), None)
    if not player or player.folded or player.all_in:
        return jsonify({"error": "Player not available for recommendation"}), 400

    # Use pre-processed range for now — will be dynamic later
    # For now: assume tight range
    # updated_ranges = get_updated_ranges(
    #     players=game_instance.players,
    #     big_blind=game_instance.big_blind,
    #     dealer_position=game_instance.dealer_position,
    #     initial_ranges=updated_ranges,
    # )
    updated_ranges = game_instance.updated_ranges
    
    hero_hand = player.hole_cards
    turn = game_instance.community_cards[:4]

    opponent_ranges = {
        pos: rng for pos, rng in updated_ranges.items()
        if pos != determine_position(
            (player.position - game_instance.dealer_position) % len(game_instance.players),
            len(game_instance.players)
        )
    }
    print("inside turn recommendation")
    print("updated_ranges: ", updated_ranges)
    print("opponent_ranges: ", opponent_ranges)

    equity_results = recommend_action(
        hero_hand=hero_hand,
        community=turn,
        updated_opponent_range=opponent_ranges,
        round="turn",
    )   
    print("equity_results: ", equity_results)

    return jsonify({
        "opponent_ranges": opponent_ranges,
        "equity_results": equity_results,
    })

@app.route("/reset", methods=["POST"])
def reset_game():
    """
    Reset the game state.
    """
    global game_instance, config_locked
    game_instance = None
    config_locked = False
    print("Game has been reset")
    return jsonify({"message": "Game reset successful"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)