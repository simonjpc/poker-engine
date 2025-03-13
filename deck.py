import random

class Deck:
    
    def __init__(self):
        self.remaining_cards = [
        "2h", "2d", "2c", "2s",
        "3h", "3d", "3c", "3s",
        "4h", "4d", "4c", "4s",
        "5h", "5d", "5c", "5s",
        "6h", "6d", "6c", "6s",
        "7h", "7d", "7c", "7s",
        "8h", "8d", "8c", "8s",
        "9h", "9d", "9c", "9s",
        "Th", "Td", "Tc", "Ts",
        "Jh", "Jd", "Jc", "Js",
        "Qh", "Qd", "Qc", "Qs",
        "Kh", "Kd", "Kc", "Ks",
        "Ah", "Ad", "Ac", "As",
        ]

    def shuffle(self):
        random.shuffle(self.remaining_cards)

    def deal(self, num_cards: int):
        cards = self.remaining_cards[:num_cards]
        self.remaining_cards = self.remaining_cards[num_cards:]
        return cards