import React, { useState, useEffect } from "react";
import Table from "./components/Table";
import HoleCardSelector from "./components/HoleCardSelector";
import FlopCardSelector from "./components/FlopCardSelector";
import TurnCardSelector from "./components/TurnCardSelector";
import { sendGameConfig, startGame, fetchGameState, resetGame } from "./api";
import "./App.css";

const DEFAULT_STACK = 20000;
const API_URL = "http://localhost:4000";
// const cards = [];

const INITIAL_PLAYERS = [
  { id: 0, name: "Anne", amount: DEFAULT_STACK, available: true },
  { id: 1, name: "Benoît", amount: DEFAULT_STACK, available: true },
  { id: 2, name: "You", amount: DEFAULT_STACK, available: true }, // This is the player controlled by the user
  { id: 3, name: "Denis", amount: DEFAULT_STACK, available: true },
  { id: 4, name: "Elodie", amount: DEFAULT_STACK, available: true },
  { id: 5, name: "François", amount: DEFAULT_STACK, available: true },
];

function App() {
  const [gameState, setGameState] = useState(null);
  const [players, setPlayers] = useState(INITIAL_PLAYERS);
  const [buttonPlayerId, setButtonPlayerId] = useState(0);
  const [gameStarted, setGameStarted] = useState(false);
  const [activePlayer, setActivePlayer] = useState(null);
  const [resetSignal, setResetSignal] = useState(false);
  const [cardInput, setCardInput] = useState("");  // 4-letter string
  const [flopInput, setFlopInput] = useState("");  // 6-letter string
  const [turnInput, setTurnInput] = useState("");  // 2-letter string
  const [waitingForFlop, setWaitingForFlop] = useState(false);
  const [waitingForTurn, setWaitingForTurn] = useState(false);

  useEffect(() => {
    let isActive = true;
  
    const poll = async () => {
      if (!isActive) return;
      const state = await fetchGameState();
      setGameState(state);
      setActivePlayer(state.active_player);

      // Wait for user to input flop if preflop is done
      if (state.awaiting_flop_input && !waitingForFlop) {
        console.log("Triggering waitingForFlop");
        setWaitingForFlop(true);
      }
      
      // Wait for user to input turn if preflop and flop is done
      if (state.awaiting_turn_input && !waitingForTurn) {
        console.log("Triggering waitingForTurn");
        setWaitingForTurn(true);
      }

      setTimeout(poll, 200);  // Reschedule next poll
    };
  
    if (gameStarted) {
      poll(); // Start polling
    }
  
    return () => {
      isActive = false; // Stop loop on unmount or game stop
    };
  }, [gameStarted]);

  useEffect(() => {
    const onKey = (e) => {
      const k = e.key?.toLowerCase?.();
      if (k === "r") {
        e.preventDefault();
        handleResetGame();
      } else if (!gameStarted && (k === "t" || k === "e")) {
        e.preventDefault();
        nudgeButton(k === "t" ? +1 : -1);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [gameStarted, players]);

  const handleUpdatePlayer = (id, updates) => {
    setPlayers((prev) =>
      prev.map((p) => (p.id === id ? { ...p, ...updates } : p))
    );
  };

  const handleStartGame = async () => {

  const parseHoleCards = (input) => {
    const rankMap = { "/": "T", "*": "J", "-": "Q", "+": "K", "0": "A" };
    const suitMap = { "u": "s", "i": "c", "o": "d", "p": "h" };

    const validSuits = ["s", "h", "d", "c"];
    const validRanks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"];
  
    if (input.length === 4) {
      const r1 = rankMap[input[0]] || input[0].toUpperCase();
      const s1 = suitMap[input[1]] || input[1];
      const r2 = rankMap[input[2]] || input[2].toUpperCase();
      const s2 = suitMap[input[3]] || input[3];
  
      if (validRanks.includes(r1) && validSuits.includes(s1) &&
          validRanks.includes(r2) && validSuits.includes(s2)) {
        return [`${r1}${convertSuit(s1)}`, `${r2}${convertSuit(s2)}`];
      }
    }
    return null;
  };


  const convertSuit = (suit) => {
    switch (suit) {
      case "s": return "♠";
      case "h": return "♥";
      case "d": return "♦";
      case "c": return "♣";
      default: return suit;
    }
  };

  const parsedCards = parseHoleCards(cardInput);

    const config = {
      players: players.map((p) => ({
        name: p.name,
        amount: p.amount,
        available: p.available,
        selectedHoleCards: p.name === "You" ? parsedCards : null,
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
    setCardInput("");
    setFlopInput("");
    setTurnInput("");
    setWaitingForFlop(false);
    setWaitingForTurn(false);
    setGameStarted(false);
    setGameState(null);
    setActivePlayer(null);
    // setPlayers(INITIAL_PLAYERS);
    setPlayers((prev) =>
        prev.map((p, i) => ({
            ...p,
            amount: gameState?.players?.[i]?.stack ?? p.amount,
        }))
    );
    setButtonPlayerId(0);
    setResetSignal(prev => !prev);
  };

  const handleSubmitFlop = async () => {
    const parseFlop = (input) => {
      const validSuits = ["s", "h", "d", "c"];
      const validRanks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"];
      const rankMap = { "/": "T", "*": "J", "-": "Q", "+": "K", "0": "A" };
      const suitMap = { "u": "s", "i": "c", "o": "d", "p": "h" };
    
      if (input.length === 6) {
        const cards = [];
        for (let i = 0; i < 3; i++) {
          const r = rankMap[input[i * 2]] || input[i * 2].toUpperCase();
          const s = suitMap[input[i * 2 + 1]] || input[i * 2 + 1];
    
          if (validRanks.includes(r) && validSuits.includes(s)) {
            cards.push(`${r}${convertSuit(s)}`);
          } else {
            return null;
          }
        }
        return cards;
      }
      return null;
    };
  
    const convertSuit = (suit) => {
      switch (suit) {
        case "s": return "♠";
        case "h": return "♥";
        case "d": return "♦";
        case "c": return "♣";
        default: return suit;
      }
    };
  
    const parsedFlop = parseFlop(flopInput);
    if (!parsedFlop) {
      alert("Invalid flop input. Use format like 8s9hjd");
      return;
    }
  
    try {
      await fetch(`${API_URL}/set_flop`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ flop_cards: parsedFlop }),
      });
  
      setFlopInput("");
      setWaitingForFlop(false);
    } catch (e) {
      console.error("Error sending flop:", e);
    }
  };

  const handleSubmitTurn = async () => {
    const parseTurn = (input) => {
      const validSuits = ["s", "h", "d", "c"];
      const validRanks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"];
      const rankMap = { "/": "T", "*": "J", "-": "Q", "+": "K", "0": "A" };
      const suitMap = { "u": "s", "i": "c", "o": "d", "p": "h" };
    
      if (input.length === 2) {
        const cards = [];
        for (let i = 0; i < 1; i++) {
          const r = rankMap[input[i * 2]] || input[i * 2].toUpperCase();
          const s = suitMap[input[i * 2 + 1]] || input[i * 2 + 1];
    
          if (validRanks.includes(r) && validSuits.includes(s)) {
            cards.push(`${r}${convertSuit(s)}`);
          } else {
            return null;
          }
        }
        return cards;
      }
      return null;
    };
  
    const convertSuit = (suit) => {
      switch (suit) {
        case "s": return "♠";
        case "h": return "♥";
        case "d": return "♦";
        case "c": return "♣";
        default: return suit;
      }
    };
  
    const parsedTurn = parseTurn(turnInput);
    console.log("Parsed Turn:", parsedTurn)
    if (!parsedTurn) {
      alert("Invalid turn input. Use format like qc");
      return;
    }
  
    try {
      await fetch(`${API_URL}/set_turn`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ turn_cards: parsedTurn }),
      });
  
      setTurnInput("");
      setWaitingForTurn(false);
    } catch (e) {
      console.error("Error sending turn:", e);
    }
  };

  const nudgeButton = (delta) => {
    if (gameStarted) return;
    setButtonPlayerId((prevId) => {
      if (!players || players.length === 0) return prevId;
  
      const currentIndex = players.findIndex(p => p.id === prevId);
      if (currentIndex === -1) return prevId;
  
      const len = players.length;
      // try up to len steps to find the next available player
      for (let step = 1; step <= len; step++) {
        const candidateIndex = (currentIndex + delta * step + len) % len;
        if (players[candidateIndex]?.available) {
          return players[candidateIndex].id;
        }
      }
      return prevId; // fallback (no available players found)
    });
  };

  const boardCount = gameState?.community_cards?.length ?? 0;

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
          boardCount={boardCount}
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
          cardInput={cardInput}
          setCardInput={setCardInput}
          disabled={gameStarted}
          onSubmit={handleStartGame}
      />)}
      {waitingForFlop && (
        <FlopCardSelector
          flopInput={flopInput}
          setFlopInput={setFlopInput}
          onSubmit={handleSubmitFlop}
          disabled={false}
        />
      )}
      {waitingForTurn && boardCount === 3 && (
        <TurnCardSelector
          turnInput={turnInput}
          setTurnInput={setTurnInput}
          onSubmit={handleSubmitTurn}
          disabled={false}
        />
      )}
      <div className="community-cards">
        {gameState?.community_cards?.map((card, index) => (
          // <span key={index} className="card">{card}</span>
          <span key={index} className={`card ${/♥|♦/.test(card) ? 'red-suit' : 'black-suit'}`}>
            {card}
          </span>
        ))}
      </div>
    </div>
  );
}

export default App;
