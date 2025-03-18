# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from game import Game

# app = Flask(__name__)
# CORS(app)  # Allow frontend to communicate with backend

# # Initialize the game with 6 players
# players = ["Anne", "Benoît", "Claire", "Denis", "Elodie", "François"]
# poker_game = Game(players, starting_stack=1000)

# @app.route('/game_state', methods=['GET'])
# def get_game_state():
#     """
#     Get the current game state, including players, stacks, and community cards.
#     """
#     game_state = {
#         "players": [{"name": p.name, "stack": p.stack, "folded": p.folded, "all_in": p.all_in} for p in poker_game.players],
#         "community_cards": poker_game.community_cards,
#         "pot": poker_game.pot,
#         "current_hand": poker_game.hand_number,
#         "dealer_position": poker_game.dealer_position
#     }
#     return jsonify(game_state)

# @app.route('/action', methods=['POST'])
# def player_action():
#     """
#     Handle player actions (fold, call, raise).
#     """
#     data = request.json
#     player_name = data.get("player")
#     action = data.get("action")
#     amount = float(data.get("amount", 0))

#     player = next((p for p in poker_game.players if p.name == player_name), None)
#     if not player:
#         return jsonify({"error": "Player not found"}), 404

#     if action == "fold":
#         player.fold_hand()
#     elif action == "call":
#         player.place_bet(amount)
#     elif action == "raise":
#         player.place_bet(amount)

#     return jsonify({"message": f"{player_name} {action}ed"})

# @app.route('/next_hand', methods=['POST'])
# def next_hand():
#     """
#     Start the next hand.
#     """
#     poker_game.play_hand()
#     return jsonify({"message": "Next hand started"})

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, jsonify, request
from flask_cors import CORS
from game import Game

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

# Initialize the game with 6 players
players = ["Anne", "Benoît", "Claire", "Denis", "Elodie", "François"]
poker_game = Game(players, starting_stack=1000)

@app.route('/game_state', methods=['GET'])
def get_game_state():
    """
    Get the current game state, including players, stacks, and community cards.
    """
    game_state = {
        "players": [{"name": p.name, "stack": p.stack, "folded": p.folded, "all_in": p.all_in} for p in poker_game.players],
        "community_cards": poker_game.community_cards,
        "pot": poker_game.pot,
        "current_hand": poker_game.hand_number,
        "dealer_position": poker_game.dealer_position
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
    amount = float(data.get("amount", 0))

    player = next((p for p in poker_game.players if p.name == player_name), None)
    if not player:
        return jsonify({"error": "Player not found"}), 404

    if action == "fold":
        player.fold_hand()
    elif action == "call":
        player.place_bet(amount)
    elif action == "raise":
        player.place_bet(amount)

    return jsonify({"message": f"{player_name} {action}ed"})

@app.route('/next_hand', methods=['POST'])
def next_hand():
    """
    Start the next hand.
    """
    poker_game.play_hand()
    return jsonify({"message": "Next hand started"})

@app.route('/start_game', methods=['POST'])
def start_game():
    """
    Start the game.
    """
    poker_game.start_game()
    return jsonify({"message": "Game started"})

if __name__ == '__main__':
    app.run(debug=True)