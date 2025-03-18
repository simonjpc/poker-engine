import React, { useState } from "react";
import { sendAction } from "../api";
import "./Player.css";

const Player = ({ player, position, dealerPosition }) => {
    const [raiseAmount, setRaiseAmount] = useState(50);

    // Define positions for the players (adjusted based on your request)
    const positions = [
        { top: "-60%", left: "40%" },  // Top-center
        { top: "-30%", left: "90%" },    // Top-right
        { top: "70%", left: "90%" },   // Bottom-right
        { top: "90%", left: "40%" },  // Bottom-center
        { top: "70%", left: "-10%" },  // Bottom-left
        { top: "-30%", left: "-10%" },   // Top-left
    ];

    return (
        <div className="player" style={positions[position]}>
            {/* Dealer Button */}
            {position === dealerPosition && <div className="dealer-button">B</div>}

            <p>{player.name}</p>
            <p>Stack: {player.stack}</p>
            {player.folded && <p>Folded</p>}
            {player.all_in && <p>All-In!</p>}

            {/* Player Actions */}
            <div className="player-actions">
                <button onClick={() => sendAction(player.name, "fold")}>Fold</button>
                <button onClick={() => sendAction(player.name, "call")}>Call</button>
                <input
                    type="number"
                    value={raiseAmount}
                    onChange={(e) => setRaiseAmount(e.target.value)}
                    className="raise-input"
                />
                <button onClick={() => sendAction(player.name, "raise", raiseAmount)}>Raise</button>
            </div>
        </div>
    );
};

export default Player;
