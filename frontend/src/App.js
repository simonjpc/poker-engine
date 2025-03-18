import React from "react";
import Table from "./components/Table";
import { startGame } from "./api";
import "./App.css";

function App() {
  const handleStartGame = async () => {
    await startGame();
  };

  return (
    <div className="App">
      <h1>Poker Engine</h1>
      <button onClick={handleStartGame}>Start Game</button>
      <Table />
    </div>
  );
}

export default App;
