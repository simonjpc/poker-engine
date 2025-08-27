import React, { useState, useEffect } from "react";
import { sendAction } from "../api";
import "./Player.css";

export default function Player({ player, onUpdate, disabled, position, dealerPosition, highestBet, active, currentStack, currentBet, isFolded, isAllIn, HoleCards, resetSignal, boardCount }) {

    const API_URL = "http://localhost:4000";
      
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

    const [suggestion, setSuggestion] = useState(null);

    useEffect(() => {
        if (active && player.name === "You") {
            fetch(`${API_URL}/game_state`)
                .then((res) => res.json())
                .then((state) => {
                    const hasFlop = state.community_cards && state.community_cards.length >= 3;
                    const endpoint = hasFlop ? "/recommend_flop_action" : "/recommend_action";
    
                    fetch(`${API_URL}${endpoint}`, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                    })
                        .then((res) => res.json())
                        .then((data) => {
                            if (!data.error) {
                                if (hasFlop) {
                                    const equity_results = data.equity_results;
                                    if (equity_results && Object.keys(equity_results).length > 0) {
                                        const formatted = Object.entries(equity_results)
                                            .map(([pos, info]) =>
                                                `${pos}: EQ ${info.equity.toFixed(1)}% (${info.outs} outs)`
                                            )
                                            .join("\n");
                                        setSuggestion(formatted);
                                    } else {
                                        setSuggestion("No opponents to evaluate");
                                    }
                                } else {
                                    setSuggestion(`${data.recommendation.toUpperCase()}${data.amount ? ` to ${data.amount}` : ''}`);
                                }
                            }
                        });
                });
        }
        return () => {};
    }, [active, boardCount]);

    useEffect(() => {
        setSuggestion(null);
    }, [resetSignal]);

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

    console.log("player:", player.name, "disabled:", disabled);

    useEffect(() => {
        if (!active) return;
      
        const handleKeyDown = (e) => {
          const key = e.key.toLowerCase();
      
          if (key === "v") {
            sendAction(player.name, "fold");
          } else if (key === "b") {
            sendAction(player.name, "call", amountToCall);
          } else if (key === "n") {
            setTimeout(() => {
              const input = document.getElementById(`raise-input-${player.name}`);
              if (input) {
                input.focus();
              }
            }, 10);
          } else if (key === "enter") {
            const input = document.getElementById(`raise-input-${player.name}`);
            if (input && document.activeElement === input && raiseAmount) {
              sendAction(player.name, "raise", raiseAmount);
              setRaiseAmount("");
            }
          }
        };
      
        window.addEventListener("keydown", handleKeyDown);
        return () => window.removeEventListener("keydown", handleKeyDown);
      }, [active, raiseAmount, amountToCall]);

    return (
        <div className="player-wrapper">
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

                {(isFolded || isAllIn) && (
                    <div className="status-badge">
                        {isFolded ? "Folded" : "All-In!"}
                    </div>
                )}

                {/* Player Actions */}
                <div className="player-actions">
                    <div className="action-row">
                        <button onClick={(e) => {
                            e.stopPropagation();
                            sendAction(player.name, "fold");
                            setSuggestion(null); }}>
                            Fold
                        </button>
                        <button onClick={(e) => {
                            e.stopPropagation(); 
                            sendAction(player.name, "call", amountToCall);
                            setSuggestion(null); }}>
                            {amountToCall > 0 ? `Call ${amountToCall}` : "Call"}
                        </button>
                    </div>
                    <div className="action-row">
                        <input
                            id={`raise-input-${player.name}`}
                            type="number"
                            value={raiseAmount}
                            onChange={(e) => setRaiseAmount(e.target.value)}
                            className="raise-input"
                            onClick={(e) => e.stopPropagation()} // in case someone clicks in the input
                        />
                        <button onClick={(e) => { 
                            e.stopPropagation(); 
                            sendAction(player.name, "raise", raiseAmount);
                            setSuggestion(null);
                            setRaiseAmount(""); }}>
                            Raise
                        </button>
                    </div>
                </div>
                {suggestion && (
                    <div className="suggestion-box-right">
                        {suggestion}
                    </div>
                )}
            </div>
        </div>
    );
};
