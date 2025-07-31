from player import Player

class BettingRound:
    """
    Manages a single betting round in No-Limit Texas Hold'em.
    Ensures correct player turn order and valid actions.
    """

    def __init__(self, players, pot, dealer_position, sb_position, bb_position, small_blind, preflop):
        """
        Initializes a new betting round.

        :param players: List of Player objects.
        :param pot: Current pot size.
        :param dealer_position: Position of the dealer button.
        :param preflop: Boolean indicating if this is the preflop round.
        """
        self.players = [p for p in players]# if not p.folded]  # Only active players
        self.pot = pot
        self.current_bet = max(p.current_bet for p in self.players)  # Track the highest bet
        self.last_raiser = None
        self.active_bets = {player: player.current_bet for player in self.players}  # Track bet amounts
        self.dealer_position = dealer_position
        self.sb_position = sb_position
        self.bb_position = bb_position
        self.preflop = preflop
        self.small_blind = small_blind

        self.current_index = 0
        self.current_player = None

        # Determine correct betting order
        self.betting_order = self.determine_betting_order()

    def determine_betting_order(self):
        """
        Determines the correct turn order based on the game phase.
        
        :return: List of players in the correct action sequence.
        """
        if self.preflop:
            # Preflop: Action starts UTG (after big blind)
            first_player = (self.dealer_position + 3) % len(self.players)  # UTG
            order = self.players[first_player:] + self.players[:first_player]
        else:
            # Postflop: First active player to the left of the dealer acts first
            first_player = (self.dealer_position + 1) % len(self.players)
            while self.players[first_player].folded:
                first_player = (first_player + 1) % len(self.players)
            order = self.players[first_player:] + self.players[:first_player]
        
        return order

    def place_bet(self, player, amount):
        """
        Handles a player placing a bet, correctly adjusting for small and big blinds.

        :param player: The Player object placing the bet.
        :param amount: The bet amount.
        """
        # Adjust current_bet based on player position (small and big blinds)
        if player.position == self.sb_position and self.preflop:  # Small Blind
            current_bet = self.current_bet - self.small_blind
        elif player.position == self.bb_position and self.preflop:  # Big Blind
            current_bet = self.current_bet - 2 * self.small_blind
        else:
            current_bet = self.current_bet

        # Allow Big Blind to check if no one raised
        if player.position == self.bb_position and amount == 0 and current_bet <= 0:
            print(f"{player.name} checks (Big Blind).")
            return

        # Handle all-in situations
        if amount < current_bet - player.current_bet:
            if amount == player.stack:  # Player is going all-in with less than the call amount
                print(f"{player.name} goes all-in with {amount} chips!")
                player.place_bet(amount)
                self.active_bets[player] += amount
                self.pot += amount
                player.all_in = True
                return
            else:
                raise ValueError(f"{player.name} must at least call the current bet of {current_bet} chips!")

        # Process the bet
        bet_amount = min(amount, player.stack)  # Can't bet more than you have
        player.place_bet(bet_amount)  # Deduct chips from player's stack
        self.active_bets[player] += bet_amount  # Update player's total bet contribution
        self.pot += bet_amount  # Add to the pot

        # If this bet is a raise, update the highest bet
        if player.current_bet > self.current_bet:
            self.current_bet = player.current_bet
            self.last_raiser = player


    def process_actions(self):
        """
        Handles a full betting round, ensuring correct betting order.
        """
        last_raiser = -1
        print([bo.name for bo in self.betting_order if not bo.folded])
        while True:
            action_taken = False  # Track if a raise occurred
            for i in range(len(self.betting_order)):
                player = self.betting_order[i]
                # Skip players who folded, are all-in, have no chips, or have already acted after the last raise
                if (player.folded or player.all_in or player.stack == 0 or 
                    (last_raiser > -1 and i >= last_raiser and not action_taken)):
                    continue

                valid_actions = self.get_valid_actions(player)
                print("valid_actions: ", valid_actions)
                if valid_actions is None:  # Player has no chips
                    continue

                action, amount = player.make_decision(valid_actions)
                self.current_index += 1
                if self.current_index >= len(self.betting_order) and action_taken:
                    self.current_index = 0
                
                if action == "fold":
                    player.fold_hand()
                elif action == "call":
                    self.place_bet(player, amount)
                elif action == "raise":
                    self.place_bet(player, amount)
                    action_taken = True  # Raise occurred, everyone gets another chance
                    last_raiser = i

            # Stop when no raises have occurred
            print("action_taken: ", action_taken)
            if not action_taken:
                break  # Betting round ends

        for player in self.players:
            player.current_bet = 0


    def find_first_active_player_postflop(self):
        """
        Finds the first active player to act postflop (first player left of dealer).
        
        :return: Index of the first active player.
        """
        first_position = (self.dealer_position + 1) % len(self.betting_order)

        while self.betting_order[first_position].folded:
            first_position = (first_position + 1) % len(self.betting_order)

        return first_position


    def find_last_active_player_before_sb(self):
        """
        Finds the last active player in the betting order before reaching the small blind again.

        :return: Index of the last active player.
        """
        sb_index = next((i for i, p in enumerate(self.betting_order) if p.position == 0), None)

        if sb_index is None:
            return len(self.betting_order) - 1  # Default to the last player if SB is missing

        # Find the last active player before the small blind
        for i in range(len(self.betting_order) - 1, -1, -1):
            if not self.betting_order[i].folded:
                return i

        return sb_index  # Fallback if all players folded



    def get_valid_actions(self, player):
        """
        Determines the legal actions a player can take.

        :param player: The Player object whose turn it is.
        :return: Dictionary of valid actions.
        """
        # Skip players with no chips (they're effectively all-in)
        if player.stack == 0:
            return None

        current_player_bet = self.active_bets[player]  # Amount this player has already committed
        amount_to_call = self.current_bet - current_player_bet  # Correct call amount

        # If player can't afford the full call amount, they can go all-in instead
        if amount_to_call > player.stack:
            amount_to_call = player.stack

        min_raise = max(self.current_bet * 2, self.current_bet + 1)  # Min raise must be double previous bet
        max_raise = player.stack  # Max raise is all-in

        valid_actions = {
            "fold": True,
            "call": amount_to_call if amount_to_call > 0 else 0,  # Ensure call amount is correct
            "raise": (min_raise, max_raise) if player.stack > amount_to_call else None
        }
        return valid_actions

    def __str__(self):
        """
        Returns a string representation of the betting round state.
        """
        return f"Pot: {self.pot} | Current Bet: {self.current_bet} | Last Raiser: {self.last_raiser.name if self.last_raiser else 'None'}"

    def get_active_player(self):
        """
        Returns the name of the player whose turn it is to act.
        """
        print("self.current_index: ", self.current_index)
        while self.current_index < len(self.betting_order):
            player = self.betting_order[self.current_index]
            if not player.folded and not player.all_in and player.stack > 0:
                return player.name
            self.current_index += 1  # Skip ineligible players

        return None  # No one left to act
    
    def perform_action(self, player, action, amount):
        if action == "fold":
            player.fold_hand()
        elif action in ["call", "raise"]:
            self.place_bet(player, amount)

        # Move to the next player
        self.current_index += 1
    
if __name__ == "__name__":

    # Create players
    player1 = Player(name="Alice", stack=1000, position=0)  # SB
    player2 = Player(name="Bob", stack=1000, position=1)  # BB
    player3 = Player(name="Charlie", stack=1000, position=2)  # UTG
    player4 = Player(name="David", stack=1000, position=3)  # MP
    player5 = Player(name="Eve", stack=1000, position=4)  # CO
    player6 = Player(name="Frank", stack=1000, position=5)  # BTN

    # Start a betting round
    betting_round = BettingRound(players=[player1, player2, player3, player4, player5, player6], pot=0, dealer_position=5, preflop=True)

    # Process betting actions
    betting_round.process_actions()

    # Print final betting state
    print(betting_round)

