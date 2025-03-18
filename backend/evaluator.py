from collections import Counter
from itertools import combinations

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
