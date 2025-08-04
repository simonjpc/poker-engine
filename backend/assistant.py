def determine_position(pos_index, num_players):
    positions = ["UTG", "MP", "CO", "BTN", "SB", "BB"]
    return positions[pos_index % len(positions)]

def classify_hand(cards):
    rank_order = "23456789TJQKA"
    r1, s1 = cards[0][0], cards[0][1]
    r2, s2 = cards[1][0], cards[1][1]

    suited = s1 == s2
    ranks = sorted([r1, r2], key=lambda r: rank_order.index(r), reverse=True)

    if r1 == r2:
        return f"{r1}{r2}"  # e.g., "77"
    return f"{ranks[0]}{ranks[1]}{'s' if suited else 'o'}"

def determine_action(position, hand, has_raiser, is_first_to_act, num_limpers, bb_value):
    """
    Determines the recommended action and raise amount based on position, hand, and previous actions.
    """
    # --- Hand Ranges by Position ---
    ranges = {
        "UTG": {
            "open_raise": {
                "pairs": [f"{r}{r}" for r in "23456789TJQKA"],
                "suited": ["ATs", "AJs", "AQs", "AKs", "KTs", "QTs", "JTs"],
                "offsuit": ["AJo", "AQo", "KQo"],
            },
            "call_vs_raise": [],
            "3bet_vs_raise": [],
        },
        "MP": {
            "open_raise": {
                "pairs": [f"{r}{r}" for r in "23456789TJQKA"],
                "suited": ["ATs", "AJs", "AQs", "AKs", "KTs", "QTs", "JTs"],
                "offsuit": ["AJo", "AQo", "KJo", "QJo"],
            },
            "call_vs_raise": [f"{r}{r}" for r in "2233445566778899TTJJQQ"] + ["KQs", "AJs", "AQs", "AKs", "AQo"],
            "3bet_vs_raise": ["AA", "KK"],
        },
        "CO": {
            "open_raise": {
                "pairs": [f"{r}{r}" for r in "23456789TJQKA"],
                "suited": ["A2s", "A3s", "A4s", "A5s", "A6s", "A7s", "A8s", "A9s", "ATs", "AJs", "AQs", "AKs", "K8s", "K9s", "KTs", "KJs", "Q8s", "Q9s", "J8s", "T8s", "96s", "86s", "75s", "65s"],
                "offsuit": ["A8o", "A9o", "ATo", "AJo", "AQo", "AKo", "K9o", "Q9o", "J9o", "T9o", "98o"],
            },
            "call_vs_raise": [f"{r}{r}" for r in "2233445566778899TTJJQQ"] + ["KQs", "ATs", "AJs", "AQs", "AKs", "KJs"],
            "3bet_vs_raise": ["AA", "KK"],
        },
        "BTN": {
            "open_raise": {
                "pairs": [f"{r}{r}" for r in "23456789TJQKA"],
                "suited": ["A2s", "A3s", "A4s", "A5s", "A6s", "A7s", "A8s", "A9s", "ATs", "AJs", "AQs", "AKs", "K2s", "K3s", "K4s", "K5s", "K6s", "K7s", "K8s", "K9s", "KTs", "KJs", "Q7s", "Q8s", "Q9s", "J7s", "T6s", "96s", "86s", "75s", "64s", "54s"],
                "offsuit": ["A2o", "A3o", "A4o", "A5o", "A6o", "A7o", "A8o", "A9o", "ATo", "AJo", "AQo", "AKo", "K7o", "Q8o", "J8o", "T8o", "98o"],
            },
            "call_vs_raise": [f"{r}{r}" for r in "2233445566778899TTJJQQ"] + ["ATs", "AJs", "AQs", "AKs", "KTs", "QTs", "JTs"],
            "3bet_vs_raise": ["AKs", "AKo", "QQ", "KK", "AA"],
        },
        "SB": {
            "open_raise": {
                "pairs": [f"{r}{r}" for r in "23456789TJQKA"],
                "suited": ["A2s", "A3s", "A4s", "A5s", "A6s", "A7s", "A8s", "A9s", "ATs", "AJs", "AQs", "AKs", "K8s", "K9s", "KTs", "Q8s", "J8s", "T8s", "96s", "86s", "75s", "65s"],
                "offsuit": ["A8o", "A9o", "ATo", "AJo", "AQo", "AKo", "K9o", "Q9o", "J9o", "T9o", "98o"],
            },
            "call_vs_raise": ["88", "99", "TT", "ATs"],
            "3bet_vs_raise": ["JJ", "QQ", "KK", "AA", "AKs", "AKo"],
        },
        "BB": {
            "open_raise": {
                "pairs": [f"{r}{r}" for r in "23456789TJQKA"],
                "suited": ["A2s", "A3s", "A4s", "A5s", "A6s", "A7s", "A8s", "A9s", "ATs", "AJs", "AQs", "AKs", "K2s", "K3s", "K4s", "K5s", "K6s", "K7s", "K8s", "K9s", "KTs", "KJs", "Q7s", "Q8s", "Q9s", "J7s", "T6s", "96s", "86s", "75s", "64s", "54s"],
                "offsuit": ["A2o", "A3o", "A4o", "A5o", "A6o", "A7o", "A8o", "A9o", "ATo", "AJo", "AQo", "AKo", "K7o", "K8o", "K9o", "Q8o", "J8o", "T8o", "98o"],
            },
            "call_vs_raise": ["88", "99", "TT", "ATs"],
            "3bet_vs_raise": ["JJ", "QQ", "KK", "AA", "AKs", "AKo"],
        },
    }

    p_rules = ranges[position]

    # First to act: use open_raise range
    if is_first_to_act:
        if hand in p_rules["open_raise"]["pairs"] or hand in p_rules["open_raise"]["suited"] or hand in p_rules["open_raise"]["offsuit"]:
            raise_amount = bb_value * 3 + (bb_value * num_limpers)
            return "raise", raise_amount
        else:
            return "fold", None

    # Not first: respond to a raise
    if hand in p_rules.get("3bet_vs_raise", []):
        base = bb_value * 3
        if position == "BTN":
            base += bb_value
        return "raise", base * 3
    elif hand in p_rules.get("call_vs_raise", []):
        return "call", None
    else:
        return "fold", None
