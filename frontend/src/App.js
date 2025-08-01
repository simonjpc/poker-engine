import React, { useState, useEffect } from "react";
import Table from "./components/Table";
import { sendGameConfig, startGame, fetchGameState, resetGame } from "./api";
import "./App.css";

const INITIAL_PLAYERS = [
  { id: 0, name: "Anne", amount: 20000, available: true },
  { id: 1, name: "Benoît", amount: 20000, available: true },
  { id: 2, name: "You", amount: 20000, available: true }, // This is the player controlled by the user
  { id: 3, name: "Denis", amount: 20000, available: true },
  { id: 4, name: "Elodie", amount: 20000, available: true },
  { id: 5, name: "François", amount: 20000, available: true },
];

function App() {
  const [gameState, setGameState] = useState(null);
  const [players, setPlayers] = useState(INITIAL_PLAYERS);
  const [buttonPlayerId, setButtonPlayerId] = useState(0);
  const [gameStarted, setGameStarted] = useState(false);
  const [activePlayer, setActivePlayer] = useState(null);

  useEffect(() => {
    if (gameStarted) {
      const interval = setInterval(async () => {
        const state = await fetchGameState();
        console.log("Fetched game state:", state);
        setGameState(state);
        setActivePlayer(state.active_player);
      }, 300);
      return () => clearInterval(interval);
    }
  }, [gameStarted]);

  const handleUpdatePlayer = (id, updates) => {
    setPlayers((prev) =>
      prev.map((p) => (p.id === id ? { ...p, ...updates } : p))
    );
  };

  const handleStartGame = async () => {
    const config = {
      players: players.map((p) => ({
        name: p.name,
        amount: p.amount,
        available: p.available,
      })),
      button_player_index: buttonPlayerId,
    };
    console.log("Sending game config:", config);
    
    try {
      console.log("Sending game config:", config);
      const res1 = await sendGameConfig(config);
      console.log("Game config sent:", res1);
    
      const res2 = await startGame();
      console.log("Game started:", res2);
    
      setGameStarted(true);
    } catch (err) {
      console.error("Error starting game:", err);
    }
  };

  const handleResetGame = async () => {
    await resetGame();
  
    // Reset frontend state
    setGameStarted(false);
    setGameState(null);
    setActivePlayer(null);
    setPlayers(INITIAL_PLAYERS);
    setButtonPlayerId(0);
  };

  return (
    <div className="App">
      <h1 className="title">Poker Table</h1>
      <Table
        players={players}
        onUpdatePlayer={handleUpdatePlayer}
        disabled={gameStarted}
        buttonPlayerId={buttonPlayerId}
        onSetButton={setButtonPlayerId}
        highestBet={gameState?.highest_bet || 0}
        playerBets={gameState?.players || []}
        activePlayer={activePlayer}
      />
      <button
        className="start-button"
        onClick={handleStartGame}
        disabled={gameStarted}
      >
        Start Game
      </button>
      <button
        className="reset-button"
        onClick={handleResetGame}
      >
        Reset Game
      </button>
    </div>
  );
}

export default App;
