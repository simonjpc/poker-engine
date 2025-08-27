# --- Hand Ranges by Position ---

POSITION_RANGES = {
    "UTG": {
        "pairs": [f"{r}{r}" for r in "23456789TJQKA"],
        "not_pairs": ["ATs", "AJs", "AQs", "AKs", "KTs", "KJs", "KQs", "QJs", "QTs", "JTs", "AJo", "AQo", "AKo", "KQo"]},
    "MP": {
        "pairs": [f"{r}{r}" for r in "23456789TJQKA"],
        "not_pairs": ["ATs", "AJs", "AQs", "AKs", "KTs", "KJs", "KQs", "QTs", "QJs", "JTs", "AJo", "AQo", "AKo", "KQo"]},
    "CO": {
        "pairs": [f"{r}{r}" for r in "23456789TJQKA"],
        "not_pairs": ["A2s", "A3s", "A4s", "A5s", "A6s", "A7s", "A8s", "A9s", "ATs", "AJs", "AQs", "AKs", "K8s", "K9s", "KTs", "KJs", "KQs", "Q8s", "Q9s", "QTs", "QJs", "J8s", "J9s", "JTs", "T8s", "T9s", "96s", "97s", "98s", "86s", "87s", "75s", "76s", "65s", "A8o", "A9o", "ATo", "AJo", "AQo", "AKo", "K9o", "KTo", "KJo", "KQo", "Q9o", "QTo", "QJo", "J9o", "JTo", "T9o", "98o"]},
    "BTN": {
        "pairs": [f"{r}{r}" for r in "23456789TJQKA"],
        "not_pairs": ["A2s", "A3s", "A4s", "A5s", "A6s", "A7s", "A8s", "A9s", "ATs", "AJs", "AQs", "AKs", "K2s", "K3s", "K4s", "K5s", "K6s", "K7s", "K8s", "K9s", "KTs", "KJs", "KQs", "Q7s", "Q8s", "Q9s", "QTs", "QJs", "J7s", "J8s", "J9s", "JTs", "T6s", "T7s", "T8s", "T9s", "96s", "97s", "98s", "86s" "87s", "75s", "76s", "64s", "65s", "54s"] + ["A2o", "A3o", "A4o", "A5o", "A6o", "A7o", "A8o", "A9o", "ATo", "AJo", "AQo", "AKo", "K7o", "K8o", "K9o", "KTo", "KJo", "KQo", "Q8o", "Q9o", "QTo", "QJo", "J8o", "J9o", "JTo", "T8o", "T9o", "98o", "QQ"]},
    "SB": {
        "pairs": [f"{r}{r}" for r in "23456789TJQKA"],
        "not_pairs": ["A2s", "A3s", "A4s", "A5s", "A6s", "A7s", "A8s", "A9s", "ATs", "AJs", "AQs", "AKs", "K8s", "K9s", "KTs", "KJs", "KQs", "Q8s", "Q9s", "QTs", "QJs", "J8s", "J9s", "JTs", "T8s", "T9s", "96s", "97s", "98s", "86s", "87s", "75s", "76s", "65s", "A8o", "A9o", "ATo", "AJo", "AQo", "AKo", "K9o", "KTo", "KJo", "KQo", "Q9o", "QTo", "QJo", "J9o", "JTo", "T9o", "98o"]},
    "BB": {
        "pairs": [f"{r}{r}" for r in "23456789TJQKA"],
        "not_pairs": ["A2s", "A3s", "A4s", "A5s", "A6s", "A7s", "A8s", "A9s", "ATs", "AJs", "AQs", "AKs", "K2s", "K3s", "K4s", "K5s", "K6s", "K7s", "K8s", "K9s", "KTs", "KJs", "KQs", "Q7s", "Q8s", "Q9s", "QTs", "QJs", "J7s", "J8s", "J9s", "JTs", "T6s", "T7s", "T8s", "T9s", "96s", "97s", "98s", "86s" "87s", "75s", "76s", "64s", "65s", "54s" + "A2o", "A3o", "A4o", "A5o", "A6o", "A7o", "A8o", "A9o", "ATo", "AJo", "AQo", "AKo", "K7o", "K8o", "K9o", "KTo", "KJo", "KQo", "Q8o", "Q9o", "QTo", "QJo", "J8o", "J9o", "JTo", "T8o", "T9o", "98o"]},
}

PREFLOP_BET_RANGES = {
    "UTG": {
        "open_raise": {
            "pairs": [f"{r}{r}" for r in "23456789TJQKA"],
            "suited": ["ATs", "AJs", "AQs", "AKs", "KTs", "KJs", "KQs", "QJs", "QTs", "JTs"],
            "offsuit": ["AJo", "AQo", "AKo", "KQo"],
        },
        "call_vs_raise": [],
        "3bet_vs_raise": [],
    },
    "MP": {
        "open_raise": {
            "pairs": [f"{r}{r}" for r in "23456789TJQKA"],
            "suited": ["ATs", "AJs", "AQs", "AKs", "KTs", "KJs", "KQs", "QTs", "QJs", "JTs"],
            "offsuit": ["AJo", "AQo", "AKo", "KQo"],
        },
        "call_vs_raise": [f"{r}{r}" for r in "23456789TJQ"] + ["KQs", "AJs", "AQs", "AKs", "AQo", "AKo"],
        "3bet_vs_raise": ["AA", "KK"],
    },
    "CO": {
        "open_raise": {
            "pairs": [f"{r}{r}" for r in "23456789TJQKA"],
            "suited": ["A2s", "A3s", "A4s", "A5s", "A6s", "A7s", "A8s", "A9s", "ATs", "AJs", "AQs", "AKs", "K8s", "K9s", "KTs", "KJs", "KQs", "Q8s", "Q9s", "QTs", "QJs", "J8s", "J9s", "JTs", "T8s", "T9s", "96s", "97s", "98s", "86s", "87s", "75s", "76s", "65s"],
            "offsuit": ["A8o", "A9o", "ATo", "AJo", "AQo", "AKo", "K9o", "KTo", "KJo", "KQo", "Q9o", "QTo", "QJo", "J9o", "JTo", "T9o", "98o"],
        },
        "call_vs_raise": [f"{r}{r}" for r in "23456789TJQ"] + ["KJs", "KQs", "ATs", "AJs", "AQs", "AKs", "QJs", "AQo", "AKo"],
        "3bet_vs_raise": ["AA", "KK"],
    },
    "BTN": {
        "open_raise": {
            "pairs": [f"{r}{r}" for r in "23456789TJQKA"],
            "suited": ["A2s", "A3s", "A4s", "A5s", "A6s", "A7s", "A8s", "A9s", "ATs", "AJs", "AQs", "AKs", "K2s", "K3s", "K4s", "K5s", "K6s", "K7s", "K8s", "K9s", "KTs", "KJs", "KQs", "Q7s", "Q8s", "Q9s", "QTs", "QJs", "J7s", "J8s", "J9s", "JTs", "T6s", "T7s", "T8s", "T9s", "96s", "97s", "98s", "86s" "87s", "75s", "76s", "64s", "65s", "54s"],
            "offsuit": ["A2o", "A3o", "A4o", "A5o", "A6o", "A7o", "A8o", "A9o", "ATo", "AJo", "AQo", "AKo", "K7o", "K8o", "K9o", "KTo", "KJo", "KQo", "Q8o", "Q9o", "QTo", "QJo", "J8o", "J9o", "JTo", "T8o", "T9o", "98o"],
        },
        "call_vs_raise": [f"{r}{r}" for r in "23456789TJQ"] + ["ATs", "AJs", "AQs", "KTs", "KJs", "KQs", "QTs", "QJs", "JTs", "AQo"],
        "3bet_vs_raise": ["AKs", "AKo", "QQ", "KK", "AA"],
    },
    "SB": {
        "open_raise": {
            "pairs": [f"{r}{r}" for r in "23456789TJQKA"],
            "suited": ["A2s", "A3s", "A4s", "A5s", "A6s", "A7s", "A8s", "A9s", "ATs", "AJs", "AQs", "AKs", "K8s", "K9s", "KTs", "KJs", "KQs", "Q8s", "Q9s", "QTs", "QJs", "J8s", "J9s", "JTs", "T8s", "T9s", "96s", "97s", "98s", "86s", "87s", "75s", "76s", "65s"],
            "offsuit": ["A8o", "A9o", "ATo", "AJo", "AQo", "AKo", "K9o", "KTo", "KJo", "KQo", "Q9o", "QTo", "QJo", "J9o", "JTo", "T9o", "98o"],
        },
        "call_vs_raise": ["88", "99", "TT", "ATs", "AJs", "AQs"],
        "3bet_vs_raise": ["JJ", "QQ", "KK", "AA", "AKs", "AKo"],
    },
    "BB": {
        "open_raise": {
            "pairs": [f"{r}{r}" for r in "23456789TJQKA"],
            "suited": ["A2s", "A3s", "A4s", "A5s", "A6s", "A7s", "A8s", "A9s", "ATs", "AJs", "AQs", "AKs", "K2s", "K3s", "K4s", "K5s", "K6s", "K7s", "K8s", "K9s", "KTs", "KJs", "KQs", "Q7s", "Q8s", "Q9s", "QTs", "QJs", "J7s", "J8s", "J9s", "JTs", "T6s", "T7s", "T8s", "T9s", "96s", "97s", "98s", "86s" "87s", "75s", "76s", "64s", "65s", "54s"],
            "offsuit": ["A2o", "A3o", "A4o", "A5o", "A6o", "A7o", "A8o", "A9o", "ATo", "AJo", "AQo", "AKo", "K7o", "K8o", "K9o", "KTo", "KJo", "KQo", "Q8o", "Q9o", "QTo", "QJo", "J8o", "J9o", "JTo", "T8o", "T9o", "98o"],
        },
        "call_vs_raise": ["88", "99", "TT", "ATs", "AJs", "AQs"],
        "3bet_vs_raise": ["JJ", "QQ", "KK", "AA", "AKs", "AKo"],
    },
}
