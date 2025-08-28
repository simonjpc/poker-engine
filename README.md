# poker-engine
No-Limit Texas Hold'em poker engine for simulation and training

## Description

This is not the traditional engine where cards are dealt randomly 
simulating a real poker game.

Instead, this engine allows to input holy cards and community cards as
well as betting decision for all the players manually. The engine 
recommends which actions to take based on:

- The holy cards and betting decisions of all players for the preflop round
- The holy cards, betting decisions and community cards for the flop and postflop round

## Notes

- Currently the engine works until the flop round. Turn and river rounds have not been developed yet (WIP).
- Frontend and backend must be launched separately. This will be optimized in further versions

## Components

Please refer to the backend and frontend descriptions for a 
detailed description of the components.

## How to make it work

### Frontend

Go to the frontend folder with `cd frontend` and execute `npm start`

### Backend

Go to the frontend folder with `cd backend` and execute `python app.py`

Additionally, you could launch the backend with gunicorn by doing `gunicorn -w 1 -b 0.0.0.0:4000 app:app` (note that the engine works only for 1 worker. It might crash when the -w argument is different than 1)

