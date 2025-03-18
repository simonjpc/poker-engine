import React, { useEffect, useState } from "react";
import { fetchGameState } from "../api";
import Player from "./Player";
import "./Table.css"; // Import styles for better layout

const Table = () => {
    const [gameState, setGameState] = useState(null);

    useEffect(() => {
        const loadGame = async () => {
            const data = await fetchGameState();
            setGameState(data);
        };
        loadGame();
    }, []);

    const handleNextHand = async () => {
        await startNextHand();
        const data = await fetchGameState();
        setGameState(data);
    };

    if (!gameState) return <div>Loading...</div>;

    return (
        <div className="table-container">
            <div className="poker-table">
                {gameState.players.map((player, index) => (
                    <Player key={index} player={player} position={index} dealerPosition={gameState.dealer_position} />
                ))}
                <div className="pot">Pot: {gameState.pot} Chips</div>
            </div>
            <button onClick={handleNextHand}>Next Hand</button>
        </div>
    );
};

export default Table;
