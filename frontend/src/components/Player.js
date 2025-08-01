import React, { useState } from "react";
import { sendAction } from "../api";
import "./Player.css";

export default function Player({ player, onUpdate, disabled, position, dealerPosition, highestBet, active, currentStack, currentBet, isFolded, isAllIn, HoleCards }) {
    const handleAmountChange = (e) => {
        const value = e.target.value;
      
        // Allow empty string while typing
        if (value === "") {
            onUpdate(player.id, { amount: "" });
        } else {
            const parsed = parseInt(value);
            if (!isNaN(parsed)) {
                onUpdate(player.id, { amount: parsed });
           }
        }
    };
    
    const handleAmountBlur = () => {
        if (player.amount === "") {
           onUpdate(player.id, { amount: 0 });
        }
    };

    const handleToggleAvailable = () => {
        onUpdate(player.id, { available: !player.available });
    };

    const [raiseAmount, setRaiseAmount] = useState("");

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
            <div className="hole-cards-and-button">
                <div className="hole-cards">
                    {(HoleCards?.length > 0 ? HoleCards : [" ", " "]).map((card, index) => (
                        <span key={index} className="card">{card}</span>
                    ))}
                </div>
                {position === dealerPosition && <div className="dealer-button">B</div>}
            </div>
                <div className="player-header">
            <strong>{player.name}</strong>
            </div>
            <div className="player-body">
                <div className="player-amount-row">
                    <label>
                        Amount:
                        <input
                            type="number"
                            className="amount-input"
                            value={player.amount}
                            onChange={handleAmountChange}
                            onBlur={handleAmountBlur}
                            style={{ width: "60px" }}
                        />
                    </label>
                </div>
                <label onClick={(e) => e.stopPropagation()}>
                    <input
                        type="checkbox"
                        checked={player.available}
                        onChange={handleToggleAvailable}
                        style={{ width: "30px", height: "30px" }}
                    />
                    Available
                </label>
            </div>

            <p>Stack: {currentStack}</p>
            <p>In Pot: {currentBet}</p>
            {/* {isFolded && <p>Folded</p>}
            {isAllIn && <p>All-In!</p>} */}
            {(isFolded || isAllIn) && (
                <div className="status-badge">
                    {isFolded ? "Folded" : "All-In!"}
                </div>
            )}

            {/* Player Actions */}
            <div className="player-actions">
                <div className="action-row">
                    <button onClick={(e) => { e.stopPropagation(); sendAction(player.name, "fold"); }}>
                        Fold
                    </button>
                    <button onClick={(e) => { e.stopPropagation(); sendAction(player.name, "call", amountToCall); }}>
                        {amountToCall > 0 ? `Call ${amountToCall}` : "Call"}
                    </button>
                </div>
                <div className="action-row">
                    <input
                        type="number"
                        value={raiseAmount}
                        onChange={(e) => setRaiseAmount(e.target.value)}
                        className="raise-input"
                        onClick={(e) => e.stopPropagation()} // in case someone clicks in the input
                    />
                    <button onClick={(e) => { e.stopPropagation(); sendAction(player.name, "raise", raiseAmount); }}>
                        Raise
                    </button>
                </div>
            </div>
        </div>
    );
};
