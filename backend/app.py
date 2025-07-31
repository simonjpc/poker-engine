from flask import Flask, jsonify, request
from flask_cors import CORS
from game import Game
import threading

app = Flask(__name__)
CORS(app, supports_credentials=True)

game_instance = None
config_locked = False

# Initialize the game with 6 players
# players = ["Anne", "Benoît", "Claire", "Denis", "Elodie", "François"]
# poker_game = Game(players, starting_stacks=[1000] * len(players))

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
                "players": [{"name": p.name, "stack": p.stack, "folded": p.folded, "all_in": p.all_in, "current_bet": p.current_bet} for p in game_instance.players],
                "community_cards": game_instance.community_cards,
                "pot": game_instance.pot,
                "current_hand": game_instance.hand_number,
                "dealer_position": game_instance.dealer_position,
                "active_player": active_player_name,
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
    active_players = [
        (p["name"], p["amount"]) for i, p in enumerate(players_config) if p["available"]
    ]

    names = [p[0] for p in active_players]
    stacks = [p[1] for p in active_players]
    game_instance = Game(players=names, starting_stacks=stacks)
    print("✅ Game instance created.")
    game_instance.dealer_position = button_index

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

@app.route("/state", methods=["GET"])
def game_state():
    print("/state endpoint was hit")
    if not game_instance:
        return jsonify({"error": "Game not started"}), 400

    players = []
    for p in game_instance.players:
        players.append({
            "name": p.name,
            "stack": p.stack,
            "current_bet": p.current_bet,
            "folded": p.folded,
            "all_in": p.all_in,
        })

    highest_bet = max((p["current_bet"] for p in players), default=0)

    return jsonify({
        "players": players,
        "highest_bet": highest_bet
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
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=4000, debug=True)