# class Game:
#     # TODO
#     def __init__(self, num_players: int, starting_stack: float):
#         self.num_players = num_players
#         self.starting_stack = starting_stack

#     def start_hand(self):
#         pass

#     def next_phase(self):
#         pass

#     def showdown(self):
#         pass

#     def reset_hand(self):
#         pass


from player import Player
from deck import Deck
from betting import BettingRound
from evaluator import HandEvaluator

class Game:
    """
    Manages the entire game of No-Limit Texas Hold’em.
    Handles player actions, betting rounds, community cards, and the showdown.
    """

    def __init__(self, players, starting_stack):
        """
        Initializes a new poker game.

        :param players: List of player names.
        :param starting_stack: The amount of chips each player starts with.
        """
        self.players = [Player(name, starting_stack, i) for i, name in enumerate(players)]
        self.deck = Deck()  # Create a deck instance
        self.community_cards = []  # Store community cards
        self.pot = 0  # Main pot
        self.small_blind = 10
        self.big_blind = 20
        self.dealer_position = 0  # Track the dealer position
        self.current_betting_round = None  # Stores the current betting round
        self.hand_number = 0  # Keeps track of how many hands have been played

    def start_game(self, max_hands=10):
        """
        Runs a full poker game for a specified number of hands.

        :param max_hands: Number of hands to play before ending the game.
        """
        for _ in range(max_hands):
            self.play_hand()
            if self.check_game_over():
                break  # Stop the game if only one player remains
        print("\nGame Over!")

    def play_hand(self):
        """
        Manages a single hand of poker from dealing to showdown.
        """
        self.hand_number += 1
        print(f"\n=== Hand {self.hand_number} ===")

        self.reset_hand()
        self.deck.shuffle()
        self.assign_blinds()
        self.deal_hole_cards()
        self.execute_betting_round("Preflop")

        if self.hand_continues():
            self.deal_community_cards(3, "Flop")
            self.execute_betting_round("Flop")

        if self.hand_continues():
            self.deal_community_cards(1, "Turn")
            self.execute_betting_round("Turn")

        if self.hand_continues():
            self.deal_community_cards(1, "River")
            self.execute_betting_round("River")

        if self.hand_continues():
            self.showdown()

        self.reset_players_for_next_hand()
        self.rotate_dealer()

    def reset_hand(self):
        """
        Prepares the game state for a new hand.
        """
        self.community_cards = []
        self.pot = 0
        self.deck.reset_deck()
        for player in self.players:
            player.reset_for_new_hand()

    def assign_blinds(self):
        """
        Assigns the small and big blinds.
        """
        small_blind_player = self.players[(self.dealer_position + 1) % len(self.players)]
        big_blind_player = self.players[(self.dealer_position + 2) % len(self.players)]

        small_blind_player.place_bet(self.small_blind)
        big_blind_player.place_bet(self.big_blind)

        self.pot += self.small_blind + self.big_blind
        print(f"\nBlinds: {small_blind_player.name} posts {self.small_blind}, {big_blind_player.name} posts {self.big_blind}")

    def deal_hole_cards(self):
        """
        Deals two private cards to each active player.
        """
        for player in self.players:
            if not player.folded:
                player.receive_cards(self.deck.deal(2))
                print(f"{player.name} receives two hole cards.")

    def deal_community_cards(self, num_cards, round_name):
        """
        Deals a set number of community cards.

        :param num_cards: Number of cards to deal.
        :param round_name: The name of the betting round (Flop, Turn, River).
        """
        new_cards = self.deck.deal(num_cards)
        self.community_cards.extend(new_cards)
        print(f"\n{round_name} dealt: {', '.join(self.community_cards)}")

    def execute_betting_round(self, round_name, preflop=False):
        """
        Manages a full betting round with correct player order.
        
        :param round_name: The name of the betting phase (Preflop, Flop, Turn, River).
        :param preflop: Boolean flag to indicate if this is a preflop round (changes action order).
        """
        print(f"\n--- {round_name} Betting Round ---")
        if "preflop" in round_name.lower():
            preflop = True
        self.current_betting_round = BettingRound(
            players=self.players, 
            pot=self.pot, 
            dealer_position=self.dealer_position, 
            small_blind=self.small_blind,
            preflop=preflop,
        )

        self.current_betting_round.process_actions()
        self.pot = self.current_betting_round.pot  # Update the total pot

    def hand_continues(self):
        """
        Determines if the hand should continue or end.
        Ends early if all but one player folds OR if remaining players are all-in.
        """
        active_players = [p for p in self.players if not p.folded]
        
        # If only one player remains, hand is over
        if len(active_players) == 1:
            winner = active_players[0]
            winner.stack += self.pot
            print(f"\n{winner.name} wins the pot of {self.pot} chips!")
            self.pot = 0
            return False
        
        # If all active players are all-in, no further betting rounds needed
        if all(p.all_in for p in active_players):
            print("\nAll remaining players are all-in. Moving to showdown...")
            return True

        return True

    def calculate_side_pots(self):
        """
        Handles side pots for players who are all-in with different stack sizes.
        """
        all_bets = sorted(set(p.current_bet for p in self.players if p.current_bet > 0))
        side_pots = []
        previous_bet = 0
        
        for bet in all_bets:
            involved_players = [p for p in self.players if p.current_bet >= bet]
            side_pot = (bet - previous_bet) * len(involved_players)
            side_pots.append((side_pot, involved_players))
            previous_bet = bet
        
        return side_pots

    def showdown(self):
        """
        Determines the winner(s) and distributes the pot.
        """
        print("\n--- Showdown ---")
        # active_players = [(p.name, p.hole_cards) for p in self.players if not p.folded]
        
        # if len(active_players) == 1:
        #     # Only one player left, they win the whole pot
        #     winner = active_players[0][0]
        #     self.players[winner].stack += self.pot
        #     print(f"{winner} wins the pot of {self.pot} chips!")
        #     return

        side_pots = self.calculate_side_pots()
        for pot, involved_players in side_pots:
            winners = HandEvaluator.compare_hands([(p.name, p.hole_cards) for p in involved_players], self.community_cards)
            split_pot = pot // len(winners)
            
            for player in self.players:
                if player.name in winners:
                    player.stack += split_pot
                    print(f"{player.name} wins {split_pot} chips!")

        self.pot = 0


    def rotate_dealer(self):
        """
        Moves the dealer button to the next player.
        """
        self.dealer_position = (self.dealer_position + 1) % len(self.players)

    def reset_players_for_next_hand(self):
        """
        Prepares players for the next hand by resetting temporary attributes.
        """
        for player in self.players:
            player.reset_for_new_hand()

    def check_game_over(self):
        """
        Checks if the game should end (i.e., only one player remains).

        :return: True if the game is over, False otherwise.
        """
        active_players = [p for p in self.players if p.stack > 0]
        if len(active_players) == 1:
            print(f"\n🏆 {active_players[0].name} is the winner with {active_players[0].stack} chips!")
            return True
        return False

if __name__ == "__main__":

    # Create a game with 3 players and 1000 chips each
    players = ["Anne", "Benoît", "Claire", "Denis", "Elodie", "François"]
    poker_game = Game(players, starting_stack=1000)

    # Start the game for up to 10 hands
    poker_game.start_game(max_hands=10)
