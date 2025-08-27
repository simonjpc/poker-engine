from treys import Evaluator, Card, Deck
from collections import Counter
from itertools import combinations, product

class HandEvaluator:
    """
    Evaluates poker hands and determines the winning hand(s).
    """

    HAND_RANKINGS = {
        "High Card": 1,
        "One Pair": 2,
        "Two Pair": 3,
        "Three of a Kind": 4,
        "Straight": 5,
        "Flush": 6,
        "Full House": 7,
        "Four of a Kind": 8,
        "Straight Flush": 9,
        "Royal Flush": 10
    }

    SUIT_LETTERS = ["s", "h", "d", "c"]
    SUIT_SYMBOMS_TO_LETTERS = {
        "♠": "s",
        "♥": "h",
        "♦": "d",
        "♣": "c",
    }
    SUIT_LETTERS_TO_SYMBOLS = {v: k for k, v in SUIT_SYMBOMS_TO_LETTERS.items()}

    @staticmethod
    def evaluate_hand(hole_cards, community_cards):
        """
        Evaluates the best 5-card hand possible from a player's hole cards and the community cards.

        :param hole_cards: List of 2 hole cards (e.g., ["A♠", "K♦"])
        :param community_cards: List of up to 5 community cards (e.g., ["10♠", "J♠", "Q♠", "K♠", "9♠"])
        :return: Tuple (hand rank name, sorted 5-card best hand)
        """
        all_cards = hole_cards + community_cards
        all_combinations = list(combinations(all_cards, 5))  # Get all possible 5-card hands
        best_hand = max(all_combinations, key=HandEvaluator.rank_hand)
        hand_rank = HandEvaluator.classify_hand(best_hand)

        return hand_rank, sorted(best_hand, key=HandEvaluator.card_value, reverse=True)

    @staticmethod
    def classify_hand(hand):
        """
        Classifies a 5-card hand into its poker hand ranking.

        :param hand: A list of 5 card strings (e.g., ["10♠", "J♠", "Q♠", "K♠", "9♠"])
        :return: The name of the hand rank (e.g., "Straight Flush")
        """
        values = sorted([HandEvaluator.card_value(card) for card in hand], reverse=True)
        suits = [card[-1] for card in hand]  # Extract suit symbols
        value_counts = Counter(values)
        unique_values = list(value_counts.keys())

        # Royal Flush
        if HandEvaluator.is_straight(values) and HandEvaluator.is_flush(hand) and max(values) == 14:
            return "Royal Flush"
        
        # Straight Flush
        if HandEvaluator.is_straight(values) and HandEvaluator.is_flush(hand):
            return "Straight Flush"
        
        # Four of a Kind
        if 4 in value_counts.values():
            return "Four of a Kind"
        
        # Full House
        if sorted(value_counts.values()) == [2, 3]:
            return "Full House"
        
        # Flush
        if HandEvaluator.is_flush(hand):
            return "Flush"
        
        # Straight
        if HandEvaluator.is_straight(values):
            return "Straight"
        
        # Three of a Kind
        if 3 in value_counts.values():
            return "Three of a Kind"
        
        # Two Pair
        if list(value_counts.values()).count(2) == 2:
            return "Two Pair"
        
        # One Pair
        if 2 in value_counts.values():
            return "One Pair"
        
        # High Card
        return "High Card"

    @staticmethod
    def is_flush(hand):
        """
        Checks if all 5 cards have the same suit.

        :param hand: A list of 5 card strings (e.g., ["10♠", "J♠", "Q♠", "K♠", "9♠"])
        :return: True if the hand is a flush, False otherwise.
        """
        suits = [card[-1] for card in hand]
        return len(set(suits)) == 1

    @staticmethod
    def is_straight(values):
        """
        Checks if a list of values represents a straight.

        :param values: A sorted list of numeric card values.
        :return: True if the hand is a straight, False otherwise.
        """
        if values == [14, 5, 4, 3, 2]:  # A-5 straight (Ace-low)
            return True
        return sorted(values) == list(range(min(values), max(values) + 1))

    @staticmethod
    def card_value(card):
        """
        Converts a card into its numeric value.

        :param card: A string representing a card (e.g., "A♠", "10♦", "K♣")
        :return: Numeric value (2-14)
        """
        rank = card[0]  # Extract the rank part (e.g., "A" from "A♠")
        rank_values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, 
                       "J": 11, "Q": 12, "K": 13, "A": 14}
        return rank_values[rank]

    @staticmethod
    def rank_hand(hand):
        """
        Returns a numerical ranking of a hand.

        :param hand: A list of 5 card strings.
        :return: Tuple (hand rank index, sorted values for tiebreaking)
        """
        values = [HandEvaluator.card_value(card) for card in hand]
        value_counts = Counter(values)
        hand_rank = HandEvaluator.classify_hand(hand)
        
        # Sort values first by frequency (descending), then by card value (descending)
        values_by_freq = []
        # First add pairs/trips/quads (frequency > 1)
        for val, count in sorted(value_counts.items(), key=lambda x: (-x[1], -x[0])):
            if count > 1:
                values_by_freq.extend([val] * count)
        # Then add kickers (frequency = 1)
        for val, count in sorted(value_counts.items(), key=lambda x: (-x[0])):
            if count == 1:
                values_by_freq.append(val)
        
        return (
            HandEvaluator.HAND_RANKINGS[hand_rank],  # Primary rank
            tuple(values_by_freq)  # Secondary rank as immutable tuple
        )

    @staticmethod
    def compare_hands(players, community_cards):
        """
        Determines the best hand among multiple players.

        :param players: List of (player_name, hole_cards) tuples.
        :param community_cards: List of 5 community cards.
        :return: List of winners.
        """
        best_rank = (0, tuple())  # Default best rank
        winners = []

        for player_name, hole_cards in players:
            hand_rank, best_hand = HandEvaluator.evaluate_hand(hole_cards, community_cards)
            hand_score = HandEvaluator.rank_hand(best_hand)

            if hand_score > best_rank:
                best_rank = hand_score
                winners = [player_name]
            elif hand_score == best_rank:
                winners.append(player_name)

        return winners
    
    def expand_notation(self, notation):
        """
        Expands shorthand notation for hands into full card representations.
        
        :param notation: A string representing a hand (e.g., "AKs", "77", "AJo").
        :return: List of full card representations.
        """
        rank1, rank2 = notation[0], notation[1]
        suited = "s" if notation[-1] == "s" else "o" if notation[-1] == "o" else None
        
        combos = []

        if rank1 == rank2:
            # Pair
            for s1, s2 in product(HandEvaluator.SUIT_LETTERS, HandEvaluator.SUIT_LETTERS):
                if s1 < s2:
                    combos.append([rank1 + s1, rank2 + s2])
        elif suited == "s":
            for s in HandEvaluator.SUIT_LETTERS:
                combos.append([rank1 + s, rank2 + s])
        elif suited == "o":
            for s1 in HandEvaluator.SUIT_LETTERS:
                for s2 in HandEvaluator.SUIT_LETTERS:
                    if s1 != s2:
                        combos.append([rank1 + s1, rank2 + s2])
        else:
            combos += self.expand_notation(rank1 + rank2 + "s")
            combos += self.expand_notation(rank1 + rank2 + "o")
        return combos
    
    def filter_dead_cards(self, combos, dead_cards):
        """
        Filters out elements that are contained in the hole cards and community cards
        
        :param combos: List of expanded card combinations
        :param dead_cards: List of cards from hole and community cards
        :return: Filtered list of combos
        """
        return [combo for combo in combos if combo[0] not in dead_cards and combo[1] not in dead_cards]
    
    def get_best_combo(self, combos, flop):
        """Evaluates the best hand from a list of card combinations and a flop using library treys
        
        :param combos: List of card combinations (2 cards)
        :param flop: List of community cards (3 cards)
        :return: Best hand from combination and associated rank
        """
        
        evaluator = Evaluator()
        nb_considered = 2
        best_combo = []
        best_score = [9999 for _ in range(nb_considered)]
        flop_cards = [Card.new(card[0] + HandEvaluator.SUIT_SYMBOMS_TO_LETTERS[card[1]]) for card in flop]

        for combo in combos:
            if len(best_combo) < nb_considered:
                best_combo.append(combo)
            else:
                hand_cards = [
                    Card.new(combo[0]),
                    Card.new(combo[1]),
                ]
                if len(set(hand_cards).intersection(set(flop_cards))):
                    score = 9999
                else:
                    score = evaluator.evaluate(hand_cards, flop_cards)
                    best_score.append(score)
                    best_score.sort()
                    score_index = best_score.index(score)
                    best_combo = best_combo[:score_index] + [combo] + best_combo[score_index + 1:]
                    best_combo = best_combo[:nb_considered]
                    best_score = best_score[:nb_considered]
        
        return best_combo[-1], best_score[-1]

    def get_best_opponent_hand(self, opponent_range, flop, hole_cards):
        
        dead_cards = flop + hole_cards
        dead_cards = [card[0] + HandEvaluator.SUIT_SYMBOMS_TO_LETTERS[card[1]] for card in dead_cards]

        all_combos = []
        for notation in opponent_range:
            expanded = self.expand_notation(notation)
            valid = self.filter_dead_cards(expanded, dead_cards)
            all_combos += valid
        best_combo, best_score = self.get_best_combo(all_combos, flop)
        
        best_hand = {
            "combo": [combo[0] + HandEvaluator.SUIT_LETTERS_TO_SYMBOLS[combo[1]] for combo in best_combo],
            "score": best_score,
        }
        
        return best_hand
    
    def compute_outs(self, hole_cards, flop, opponent_combo):
        """Computes the number of outs for a given hand against an opponent's combo
        
        :param hole_cards: List of hole cards (2 cards)
        :param flop: List of community cards (3 cards)
        :param opponent_combo: Opponent's best hand in his range (2 cards)
        :return: Number of outs
        """
        evaluator = Evaluator()
        deck = Deck()
        known_cards = flop + hole_cards + opponent_combo
        known_card_objs = [Card.new(c[0] + HandEvaluator.SUIT_SYMBOMS_TO_LETTERS[c[1]]) for c in known_cards]


        remaining_deck = [c for c in deck.cards if c not in known_card_objs]

        hole_cards = [Card.new(c[0] + HandEvaluator.SUIT_SYMBOMS_TO_LETTERS[c[1]]) for c in hole_cards]
        opponent_cards = [Card.new(c[0] + HandEvaluator.SUIT_SYMBOMS_TO_LETTERS[c[1]]) for c in opponent_combo]
        flop_cards = [Card.new(c[0] + HandEvaluator.SUIT_SYMBOMS_TO_LETTERS[c[1]]) for c in flop]

        # we could also expand this to two hands (turn, river)
        outs_one_hand = set()

        for turn in remaining_deck:
            community = flop_cards + [turn]
            player_score = evaluator.evaluate(hole_cards, community)
            opp_score = evaluator.evaluate(opponent_cards, community)

            if player_score < opp_score:
                outs_one_hand.add(turn)

        return {
            "outs_on_turn": len(outs_one_hand),
        }

if __name__ == "__main__":
    # Players' hole cards
    players = [
        ("Alice", ["A♠", "K♦"]),
        ("Bob", ["J♥", "J♣"])
    ]

    # Community cards
    community_cards = ["10♠", "J♠", "Q♠", "K♠", "9♠"]  # Straight Flush

    # Evaluate hands
    for name, hole_cards in players:
        hand_rank, best_hand = HandEvaluator.evaluate_hand(hole_cards, community_cards)
        print(f"{name}'s best hand: {hand_rank} ({best_hand})")

    # Determine the winner
    winners = HandEvaluator.compare_hands(players, community_cards)
    print("Winner(s):", winners)
