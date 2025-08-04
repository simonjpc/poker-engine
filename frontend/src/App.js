import React, { useState, useEffect } from "react";
import Table from "./components/Table";
import HoleCardSelector from "./components/HoleCardSelector";
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
  const [resetSignal, setResetSignal] = useState(false);

  const [card1, setCard1] = useState({ rank: "", suit: "" });
  const [card2, setCard2] = useState({ rank: "", suit: "" });

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

  const youHoleCards = (card1.rank && card1.suit && card2.rank && card2.suit)
    ? [`${card1.rank}${card1.suit}`, `${card2.rank}${card2.suit}`]
    : null;

  const handleStartGame = async () => {
    const config = {
      players: players.map((p) => ({
        name: p.name,
        amount: p.amount,
        available: p.available,
        selectedHoleCards: p.name === "You" ? youHoleCards : null,
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
    setResetSignal(prev => !prev);
    setCard1({ rank: "", suit: "" });  // 🔁 reset selected cards
    setCard2({ rank: "", suit: "" });
  };

  return (
    <div className="App">
      <Table
          players={players}
          onUpdatePlayer={handleUpdatePlayer}
          disabled={gameStarted}
          buttonPlayerId={buttonPlayerId}
          onSetButton={setButtonPlayerId}
          highestBet={gameState?.highest_bet || 0}
          playerBets={gameState?.players || []}
          activePlayer={activePlayer}
          resetSignal={resetSignal}
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
      {!gameStarted && (<HoleCardSelector
          card1={card1}
          card2={card2}
          setCard1={setCard1}
          setCard2={setCard2}
          disabled={gameStarted}
      />)}
    </div>
  );
}

export default App;
