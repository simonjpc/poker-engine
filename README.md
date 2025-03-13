# poker-engine
No-Limit Texas Hold'em poker engine for simulation and training

## Components

* Game State Management to track everything happening in a hand
  - Player positions (Small Blind, Big Blind, UTG, Middle Position (UTG+1), Cut-Off, Button)
  - Stack sizes and current pot size
  - Betting history and action sequence
  - Community cards and hole cards (?)

* Texas Hold'Em rules
  - Blinds and antes (?)
  - Legal bet sizes (No-Limit allows any size)
  - Valid actions (Fold, Call, Bet, Raise)
  - Side pots (if multiple players are all-in)

* Hand Evaluation to deterine the winning hand 
  - Ranks hands.
  - Handles tiebreakers and split pots.

* Betting Logic to manage betting rounds
  - Preflop  
  - Flop  
  - Turn
  - River

* Player Interaction
  - Allow players to submit actions: bet(amount), call(), fold(), check()
  - Returns updated game state after an action

* Deck & Randomization
  - Shuffles and deals cards randomly to ensure fair play.

* Logging & Debugging