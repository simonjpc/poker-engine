from player import Player
from deck import Deck
from betting import BettingRound
from evaluator import HandEvaluator

class Game:
    """
    Manages the entire game of No-Limit Texas Hold'em.
    Handles player actions, betting rounds, community cards, and the showdown.
    """

    def __init__(self, players, starting_stacks, manual_holecards=None):
        """
        Initializes a new poker game.

        :param players: List of player names.
        :param starting_stack: The amount of chips each player starts with.
        """
        self.players = [Player(name, stack, i) for i, (name, stack) in enumerate(zip(players, starting_stacks))]
        self.current_bet = max(p.current_bet for p in self.players) if self.players else 0
        self.deck = Deck()  # Create a deck instance
        self.community_cards = []  # Store community cards
        self.pot = 0  # Main pot
        self.small_blind = 10
        self.big_blind = 20
        self.dealer_position = 0  # Track the dealer position
        self.small_blind_position = (self.dealer_position + 1) % len(self.players)
        self.big_blind_position = (self.dealer_position + 2) % len(self.players)
        self.current_betting_round = None  # Stores the current betting round
        self.hand_number = 0  # Keeps track of how many hands have been played
        self.manual_holecards = manual_holecards or {}

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
        self.small_blind_player = self.players[(self.dealer_position + 1) % len(self.players)]
        self.big_blind_player = self.players[(self.dealer_position + 2) % len(self.players)]

        self.small_blind_player.place_bet(self.small_blind)
        self.big_blind_player.place_bet(self.big_blind)

        self.pot += self.small_blind + self.big_blind
        print(f"\nBlinds: {self.small_blind_player.name} posts {self.small_blind}, {self.big_blind_player.name} posts {self.big_blind}")

    def deal_hole_cards_old(self):
        """
        Deals two private cards to each active player.
        """
        for player in self.players:
            if not player.folded:
                player.receive_cards(self.deck.deal(2))
                print(f"{player.name} receives two hole cards.")

    def deal_hole_cards(self):
        for player in self.players:
            if not player.folded:
                if player.name.lower() == "you" and "you" in self.manual_holecards:
                    cards = self.manual_holecards["you"]
                    # Remove selected cards from deck
                    self.deck.cards = [c for c in self.deck.cards if c not in cards]
                    player.receive_cards(cards)
                    print(f"{player.name} receives manually selected hole cards: {cards}")
                else:
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
            sb_position=self.small_blind_position,
            bb_position=self.big_blind_position,
            small_blind=self.small_blind,
            preflop=preflop,
        )

        self.current_betting_round.process_actions() # <- line not needed for frontend, but needed if playing with terminal
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
        all_bets = sorted(set(p.current_hand_bet for p in self.players if p.current_hand_bet > 0))
        side_pots = []
        previous_bet = 0
        print([(p.name, p.current_hand_bet) for p in self.players])
        print("all_bets: ", all_bets)
        for bet in all_bets:
            involved_players = [p for p in self.players if p.current_hand_bet >= bet]
            side_pot = (bet - previous_bet) * len(involved_players)
            side_pots.append((side_pot, involved_players))
            previous_bet = bet
        
        return side_pots

    def showdown(self):
        """
        Determines the winner(s) and distributes the pot(s).
        Creates side pots when players are all-in and others continue betting.
        """
        print("\n--- Showdown ---")
        
        active_players = [p for p in self.players if not p.folded]
        for p in active_players:
            print(f"{p.name}: {p.hole_cards}")

        if len(active_players) == 1:
            winner = active_players[0]
            winner.stack += self.pot
            print(f"{winner.name} wins {self.pot} chips!")
            self.pot = 0
            return

        # Sort all bets (including partial all-in bets) to create correct pot levels
        all_bets = sorted(set(p.current_hand_bet for p in self.players if p.current_hand_bet > 0))
        previous_amount = 0
        remaining_pot = self.pot

        for bet_level in all_bets:
            # Calculate pot for this level
            current_pot = 0
            # For each player who bet something in this level
            for player in self.players:
                if player.current_hand_bet > previous_amount:
                    # Their contribution to this level is the minimum of:
                    # - their total bet
                    # - the current level amount
                    # minus what they contributed to previous levels
                    contribution = min(player.current_hand_bet, bet_level) - previous_amount
                    current_pot += contribution

            if current_pot > 0:
                # Players eligible for this pot level are those who:
                # 1. Haven't folded
                # 2. Contributed at least up to the previous_amount
                eligible_players = [p for p in active_players if p.current_hand_bet >= bet_level]
                
                if eligible_players:
                    winners = HandEvaluator.compare_hands(
                        [(p.name, p.hole_cards) for p in eligible_players],
                        self.community_cards
                    )
                    
                    split_amount = current_pot // len(winners)
                    remainder = current_pot % len(winners)
                    
                    print(f"\nPot level {bet_level} chips ({current_pot} total):")
                    for player in self.players:
                        if player.name in winners:
                            extra_chip = 1 if remainder > 0 else 0
                            remainder -= 1
                            winning_amount = split_amount + extra_chip
                            player.stack += winning_amount
                            print(f"{player.name} wins {winning_amount} chips!")
                    
                    remaining_pot -= current_pot
            
            previous_amount = bet_level
        
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
