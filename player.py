from typing import List

class Player:

    def __init__(self, position: str, stack: float, cards: List[str], name: str = None):
        self.position = position
        self.stack = stack
        self.name = name
        self.cards = cards

    def make_decision(self, valid_actions: List[str]):
        # TODO
        pass

    def update_stack(self, amount: float):
        self.stack -= amount