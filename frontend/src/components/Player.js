import React, { useState, useEffect } from "react";
import { sendAction } from "../api";
import "./Player.css";

export default function Player({ player, onUpdate, disabled, position, dealerPosition, highestBet, active, currentStack, currentBet, isFolded, isAllIn }) {
    const handleAmountChange = (e) => {
        onUpdate(player.id, { amount: parseInt(e.target.value) || 0 });
      };
    
      const handleToggleAvailable = () => {
        onUpdate(player.id, { available: !player.available });
      };

    const [validActions, setValidActions] = useState({});
    const [raiseAmount, setRaiseAmount] = useState("");
    const [callAmount, setCallAmount] = useState(0);

    // Define positions for the players (adjusted based on your request)
    const positions = [
        { top: "-60%", left: "40%" },  // Top-center
        { top: "-30%", left: "90%" },    // Top-right
        { top: "70%", left: "90%" },   // Bottom-right
        { top: "90%", left: "40%" },  // Bottom-center
        { top: "70%", left: "-10%" },  // Bottom-left
        { top: "-30%", left: "-10%" },   // Top-left
    ];

    const amountToCall = Math.max(0, highestBet - (currentBet || 0));
    console.log("Amount to call:", amountToCall);

    return (
        <div className={`player ${active ? "active-player" : ""}`} style={positions[position]}>
            <div className="player-header">
            <strong>{player.name}</strong>
            </div>
            <div className="player-body">
            <label>
                Amount:
                <input
                type="number"
                value={player.amount}
                onChange={handleAmountChange}
                />
            </label>
            <label>
                <input
                type="checkbox"
                checked={player.available}
                onChange={handleToggleAvailable}
                />
                Available
            </label>
            </div>
            {/* Dealer Button */}
            {position === dealerPosition && <div className="dealer-button">B</div>}

            <p>Stack: {currentStack}</p>
            <p>In Pot: {currentBet}</p>
            {isFolded && <p>Folded</p>}
            {isAllIn && <p>All-In!</p>}

            {/* Player Actions */}
            <div className="player-actions">
                <button onClick={() => sendAction(player.name, "fold")}>Fold</button>
                <button onClick={() => sendAction(player.name, "call", amountToCall)}>
                    {amountToCall > 0 ? `call ${amountToCall}` : "check"}
                </button>
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
