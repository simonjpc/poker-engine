class Player:
    def __init__(self, name: str, stack: int, position: int):
        """
        Initializes a poker player.

        :param name: The player's name.
        :param stack: The player's starting chip count.
        :param position: The player's seat position (0 = Small Blind, 1 = Big Blind, etc.).
        """
        self.name = name                # Player's name
        self.stack = stack              # Current chip count
        self.position = position        # Seat position at the table
        self.hole_cards = []            # Two private cards
        self.current_bet = 0            # Chips committed to the pot in the current round
        self.current_hand_bet = 0
        self.folded = False             # Whether the player has folded
        self.all_in = False             # Whether the player is all-in

    def receive_cards(self, cards: list):
        """
        Assigns hole cards to the player.

        :param cards: List of two card objects.
        """
        self.hole_cards = cards

    def make_decision(self, valid_actions, ai_model=None):
        """
        Returns an action based on available options.
        Supports AI-based decisions if an AI model is provided.
        
        :param valid_actions: Dictionary of available actions.
        :param ai_model: Optional AI model for automated decision-making.
        :return: Tuple (action: str, amount: int or None)
        """
        if ai_model:
            return ai_model.choose_action(valid_actions)  # AI chooses the best action

        # Otherwise, use manual input
        print(f"\n{self.name}'s Turn - Stack: {self.stack} | Valid actions: {valid_actions}")
        while True:
            action = input("Choose action (fold, call, raise): ").strip().lower()
            if action in valid_actions:
                if action == "raise":
                    min_raise, max_raise = valid_actions["raise"]
                    amount = int(input(f"Enter raise amount ({min_raise}-{max_raise}): "))
                    if amount > max_raise:
                        return "raise", max_raise
                    elif min_raise <= amount <= max_raise:
                        return "raise", amount
                else:
                    return action, valid_actions.get(action, None)
            print("Invalid action. Try again.")


    def place_bet(self, amount: int):
        """
        Handles the player placing a bet.

        :param amount: The number of chips being bet.
        """
        if amount >= self.stack:
            self.current_bet += self.stack  # All-in
            self.current_hand_bet += self.stack
            self.stack = 0
            self.all_in = True
            print(f"{self.name} goes all-in with {self.current_bet} chips!")
        else:
            self.stack -= amount
            self.current_bet += amount
            self.current_hand_bet += amount
            print(f"{self.name} bets {amount} chips. Remaining stack: {self.stack}")

    def fold_hand(self):
        """
        Marks the player as folded.
        """
        self.folded = True
        print(f"{self.name} folds.")

    def reset_for_new_hand(self):
        """
        Resets player attributes for the next hand.
        """
        self.hole_cards = []
        self.current_bet = 0
        self.current_hand_bet = 0
        self.folded = False
        self.all_in = False

    def __str__(self):
        """
        Returns a string representation of the player.
        """
        status = "All-in" if self.all_in else "Folded" if self.folded else f"Stack: {self.stack}"
        return f"{self.name} ({status})"


if __name__ == "__main__":
    # Create two players
    player1 = Player(name="Alice", stack=1000, position=0)
    player2 = Player(name="Bob", stack=1000, position=1)

    # Deal hole cards
    player1.receive_cards(["A♠", "K♦"])
    player2.receive_cards(["J♥", "J♣"])

    # Player makes a decision
    valid_actions = {"fold": True, "call": 100, "raise": (200, 500)}
    action, amount = player1.make_decision(valid_actions)

    # Process decision
    if action == "fold":
        player1.fold_hand()
    elif action == "call":
        player1.place_bet(amount)
    elif action == "raise":
        player1.place_bet(amount)

    # Print player status
    print(player1)
    print(player2)