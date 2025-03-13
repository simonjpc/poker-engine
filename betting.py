from typing import List
from validator import ActionValdation

class BettingRound:

    def __init__(self, players: List[str], pot: float) -> None:
        self.players = players
        self.validator = ActionValdation()

    def place_bet(self, player, amount: float):
        pass

    def process_actions(self):
        pass

    def resolve_betting(self):
        pass
    