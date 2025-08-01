import Player from "./Player";
import "./Table.css"; // Import styles for better layout

export default function Table({ players, onUpdatePlayer, disabled, buttonPlayerId, onSetButton, highestBet, playerBets, activePlayer }) {
    const radius = 250; // Radius of the circle
    const centerX = 420;
    const centerY = 120;

    const angleMap = {
        0: -40,
        1: 40,
        2: 90, // You
        3: 140,
        4: 220,
        5: 270 
    };

    return (
        <div className="table-container">
          {players.map((player, index) => {

            const angleInDegrees = angleMap[index];
            const angleInRadians = (angleInDegrees * Math.PI) / 180;

            const x = centerX + 2 * radius * Math.cos(angleInRadians);
            const y = centerY + 1.02 * radius * Math.sin(angleInRadians);

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
                    className="table-seat"
                    style={{ top: `${y}px`, left: `${x}px` }}
                    onClick={() => !disabled && onSetButton(player.id)}
                >
                    <div className="player-wrapper">
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
                            HoleCards={liveState?.hole_cards || []}
                        />
                    </div>
                </div>
            );
          })}
        </div>
      );
    }
