# import random

# class Deck:
    
#     def __init__(self):
#         self.remaining_cards = [
#         "2h", "2d", "2c", "2s",
#         "3h", "3d", "3c", "3s",
#         "4h", "4d", "4c", "4s",
#         "5h", "5d", "5c", "5s",
#         "6h", "6d", "6c", "6s",
#         "7h", "7d", "7c", "7s",
#         "8h", "8d", "8c", "8s",
#         "9h", "9d", "9c", "9s",
#         "Th", "Td", "Tc", "Ts",
#         "Jh", "Jd", "Jc", "Js",
#         "Qh", "Qd", "Qc", "Qs",
#         "Kh", "Kd", "Kc", "Ks",
#         "Ah", "Ad", "Ac", "As",
#         ]

#     def shuffle(self):
#         random.shuffle(self.remaining_cards)

#     def deal(self, num_cards: int):
#         cards = self.remaining_cards[:num_cards]
#         self.remaining_cards = self.remaining_cards[num_cards:]
#         return cards

import random

class Deck:
    def __init__(self):
        """
        Initializes a standard 52-card deck.
        """
        self.cards = self._generate_deck()  # Create a full deck
        self.shuffle()  # Shuffle the deck when initialized

    def _generate_deck(self):
        """
        Generates a standard 52-card deck.
        
        :return: List of cards in the format "RankSuit" (e.g., "As", "Td").
        """
        suits = ['s', 'h', 'd', 'c']  # Spades, Hearts, Diamonds, Clubs
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        return [rank + suit for suit in suits for rank in ranks]

    def shuffle(self):
        """
        Shuffles the deck.
        """
        random.shuffle(self.cards)

    def deal(self, num_cards: int):
        """
        Deals a specified number of cards from the deck.
        
        :param num_cards: Number of cards to deal.
        :return: List of dealt cards.
        """
        if num_cards > len(self.cards):
            raise ValueError("Not enough cards left in the deck to deal.")
        
        dealt_cards = self.cards[:num_cards]  # Take the top cards
        self.cards = self.cards[num_cards:]   # Remove them from the deck
        return dealt_cards

    def reset_deck(self):
        """
        Resets the deck back to a full 52 cards and shuffles it.
        """
        self.cards = self._generate_deck()
        self.shuffle()

    def remaining_cards(self):
        """
        Returns the number of remaining cards in the deck.
        """
        return len(self.cards)

    def __str__(self):
        """
        Returns a string representation of the deck.
        """
        return f"Deck ({len(self.cards)} cards remaining): " + ", ".join(self.cards)


if __name__ == "__main__":
    # Initialize the deck
    deck = Deck()
    print(deck)  # Show shuffled deck

    # Deal two hole cards to a player
    hole_cards = deck.deal(2)
    print("Dealt hole cards:", hole_cards)

    # Deal the flop (first 3 community cards)
    flop = deck.deal(3)
    print("Flop:", flop)

    # Deal the turn (fourth community card)
    turn = deck.deal(1)
    print("Turn:", turn)

    # Deal the river (fifth community card)
    river = deck.deal(1)
    print("River:", river)

    # Check remaining cards
    print("Remaining in deck:", deck.remaining_cards())

    # Reset the deck
    deck.reset_deck()
    print("Deck reset:", deck)
