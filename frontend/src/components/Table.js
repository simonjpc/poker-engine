import React, { useEffect, useState } from "react";
import { fetchGameState } from "../api";
import Player from "./Player";
import "./Table.css"; // Import styles for better layout

const Table = () => {
    const [gameState, setGameState] = useState(null);
    const [firstPlayerIndex, setFirstPlayerIndex] = useState(0); // Track first player

    useEffect(() => {
        const loadGame = async () => {
            const data = await fetchGameState();
            setGameState(data);

            // Assume first player is dealer + 3 (UTG), update as needed
            if (data.players.length > 0) {
                setFirstPlayerIndex((prevIndex) => (prevIndex + 1) % data.players.length);
            }
        };
        loadGame();
    }, []);

    if (!gameState) return <div>Loading...</div>;

    return (
        <div className="table-container">
            <div className="poker-table">
                {gameState.players.map((player, index) => (
                    <Player key={index} player={player} position={index} isFirst={index === firstPlayerIndex} />
                ))}
                <div className="pot">Pot: {gameState.pot} Chips</div>
            </div>
        </div>
    );
};

export default Table;
