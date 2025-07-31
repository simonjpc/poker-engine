import Player from "./Player";
import "./Table.css"; // Import styles for better layout

export default function Table({ players, onUpdatePlayer, disabled, buttonPlayerId, onSetButton, highestBet, playerBets, activePlayer }) {
    const radius = 250; // Radius of the circle
    const centerX = 420;
    const centerY = 100;
    const totalPlayers = players.length;
    return (
        <div className="table-container">
          {players.map((player, index) => {
            const angle = (2 * Math.PI * index) / totalPlayers;
            const x = centerX + 1.6 * radius * Math.cos(angle);
            const y = centerY + radius * Math.sin(angle);

            // Match player by name from /state
            console.log("Frontend Player Mapping:");
            console.log("Frontend player:", player.name);
            console.log("Backend live data:", playerBets);
            const liveState = playerBets?.find(p => p.name === player.name);
            console.log("Matched backend player:", liveState);

            console.log("Matching frontend name:", player.name);
            console.log("Against backend names:", playerBets.map(p => p.name));
            
            return (
                <div
                // key={player.id}
                className={`table-seat ${buttonPlayerId === player.id ? "button-seat" : ""}`}
                style={{ top: `${y}px`, left: `${x}px` }}
                onClick={() => !disabled && onSetButton(player.id)}
                >
                <Player
                player={player}
                onUpdate={onUpdatePlayer}
                disabled={disabled || player.name !== activePlayer} 
                position={index}
                dealerPosition={buttonPlayerId}
                highestBet={highestBet}
                active={player.name === activePlayer}
                currentStack={liveState?.stack}
                currentBet={liveState?.current_bet}
                isFolded={liveState?.folded ?? false}
                isAllIn={liveState?.all_in ?? false}
                />
                {buttonPlayerId === player.id && <div className="dealer-button">D</div>}
              </div>
            );
          })}
        </div>
      );
    }
