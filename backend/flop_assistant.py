from treys import Card
from evaluator import HandEvaluator

handevaluator = HandEvaluator()
# Sample equity map
equity_map = {
    2: {"percent_on_2_coming_cards": 8.7, "percent_on_1_coming_cards": 4.55},
    3: {"percent_on_2_coming_cards": 8.7, "percent_on_1_coming_cards": 4.55},
    4: {"percent_on_2_coming_cards": 18.5, "percent_on_1_coming_cards": 8.9},
    5: {"percent_on_2_coming_cards": 20.2, "percent_on_1_coming_cards": 11.3},
    6: {"percent_on_2_coming_cards": 24.75, "percent_on_1_coming_cards": 13.6},
    7: {"percent_on_2_coming_cards": 27.8, "percent_on_1_coming_cards": 15.9},
    8: {"percent_on_2_coming_cards": 32.6, "percent_on_1_coming_cards": 18.2},
    9: {"percent_on_2_coming_cards": 38.6, "percent_on_1_coming_cards": 20.5},
    10: {"percent_on_2_coming_cards": 39.6, "percent_on_1_coming_cards": 22.7},
    11: {"percent_on_2_coming_cards": 39.6, "percent_on_1_coming_cards": 22.7},
    12: {"percent_on_2_coming_cards": 45.0, "percent_on_1_coming_cards": 27.2},
    13: {"percent_on_2_coming_cards": 45.0, "percent_on_1_coming_cards": 27.2},
    14: {"percent_on_2_coming_cards": 45.0, "percent_on_1_coming_cards": 27.2},
    15: {"percent_on_2_coming_cards": 64.8, "percent_on_1_coming_cards": 38.3},
}

def recommend_action(hero_hand, community, updated_opponent_range, round):

    equity_results = {}

    for position, range_list in updated_opponent_range.items():
        if not range_list:
            continue # skip empty ranges
        
        # Get best possible hand from opponent's range
        best_hand = handevaluator.get_best_opponent_hand(range_list, community, hero_hand)
        best_combo = best_hand["combo"]

        # ompute outs vs. that combo
        outs_result = handevaluator.compute_outs(hero_hand, community, best_combo)
        num_outs = outs_result["outs_on_turn"]

        # Map to equity
        if num_outs > 15:
            equity = 64.8 if round == "flop" else 38.3
        else:
            equity = (
                equity_map.get(num_outs, {}).get("percent_on_2_coming_cards", 0.0)
                if round =="flop"
                else equity_map.get(num_outs, {}).get("percent_on_1_coming_cards", 0.0)
            )

        # Store
        equity_results[position] = {
            "outs": num_outs,
            "equity": equity,
            "combo": best_combo
        }

    return equity_results