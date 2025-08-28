# Backend

This folder contains the backend implementation for the poker engine. The backend is responsible for handling the game logic, evaluating poker hands, and providing recommendations based on the input data.

## Description

The backend allows users to input hole cards, community cards, and betting decisions for all players. Based on this input, it evaluates the game state and provides recommendations for actions to take during the preflop and flop rounds (WIP for turn and river).

### Key Features:
- Manual input of hole cards, community cards, and betting decisions.
- Game evaluation and action recommendations for preflop and flop rounds.
- Modular design for easy extension to turn and river rounds (WIP).

## Components

The backend consists of the following modules:

- **[`app.py`](app.py)**: Entry point for the backend application.
- **[`assistant.py`](assistant.py)**: Provides assistance and recommendations for poker actions.
- **[`betting.py`](betting.py)**: Handles betting logic and decisions.
- **[`deck.py`](deck.py)**: Manages the deck of cards and card-related operations.
- **[`evaluator.py`](evaluator.py)**: Evaluates poker hands and determines winners.
- **[`flop_assistant.py`](flop_assistant.py)**: Specialized logic for the flop round.
- **[`game.py`](game.py)**: Core game logic and state management.
- **[`player.py`](player.py)**: Represents players and their actions.
- **[`ranges.py`](ranges.py)**: Manages hand ranges per position.

## Requirements

- Python 3.13
- Dependencies listed in `requirements.txt`

## Installation

1. Navigate to the `backend` folder:
   ```bash
   cd backend
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Backend

To start the backend server, run the following command:

```bash
python app.py
```

Alternatively, you can use Gunicorn for production:

```bash
gunicorn -w 1 -b 0.0.0.0:4000 app:app
```

> **Note:** The backend currently supports only 1 worker. Using more than 1 worker (`-w` argument) may cause crashes.

### API Endpoints

The backend exposes several API endpoints for interacting with the poker engine. Refer to the code in [`app.py`](app.py) for details on available routes.

## Notes

- The backend currently supports only the preflop and flop rounds. Turn and river rounds are under development.
- Ensure the backend is running before interacting with the frontend.

## Contributing

Contributions are welcome! If you would like to contribute, please fork the repository and submit a pull request.

## License

This project is licensed under the Apache License. See the [LICENSE](../LICENSE) file for details.