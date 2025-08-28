from ranges import PREFLOP_BET_RANGES, POSITION_RANGES

def determine_position(pos_index, num_players):
    positions = ["BTN", "SB", "BB", "UTG", "MP", "CO"]
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

    p_rules = PREFLOP_BET_RANGES[position]
    print("+++++++++")
    print(f"Position: {position}")
    print("+++++++++")
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

def get_updated_ranges(players, big_blind, dealer_position):
    """
    Return a filtered dict of player ranges based on preflop actions.
    """

    updated_ranges = {}

    for player in players:
        if player.folded:
            continue

        pos_index = (player.position - dealer_position) % len(players)
        position_name = determine_position(pos_index, len(players))

        full_range = POSITION_RANGES.get(position_name, [])
        bet_range = PREFLOP_BET_RANGES.get(position_name, {})

        # Infer preflop action
        if player.current_bet == 0:
            action = "check"
        elif player.current_bet == big_blind:
            action = "call"
        elif player.current_bet > big_blind:
            action = "raise"
        else:
            action = "call"  # Covers small blind case

        # Narrow range based on action
        if action == "call":
            updated_ranges[position_name] = bet_range.get("call_vs_raise", [])
        elif action == "raise":
            # Combine open_raise and 3bet_vs_raise if desired
            raise_range = bet_range.get("open_raise", {})
            combo = (
                raise_range.get("pairs", []) +
                raise_range.get("suited", []) +
                raise_range.get("offsuit", []) +
                bet_range.get("3bet_vs_raise", [])
            )
            updated_ranges[position_name] = combo
        elif action == "check":
            # Be generous for now: assume call range
            updated_ranges[position_name] = bet_range.get("call_vs_raise", [])
        else:
            updated_ranges[position_name] = full_range  # fallback (should not happen)

    return updated_ranges