// src/components/HoleCardSelector.js
import React, { useEffect, useRef } from "react";
import "./HoleCardSelector.css";

// const suits = ["♠", "♥", "♦", "♣"];
// const ranks = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"];

export default function HoleCardSelector({ cardInput, setCardInput, disabled }) {
    const inputRef = useRef(null);
    
    useEffect(() => {
            if (!disabled && inputRef.current) {
            inputRef.current.focus(); // Autofocus when component mounts
            }
        }, [disabled]);

//   const createCardOptions = (card, setCard) => (
//     <div className="card-select-group">
//       <select
//         disabled={disabled}
//         value={card.rank}
//         onChange={(e) => setCard({ ...card, rank: e.target.value })}
//       >
//         <option value="">Rank</option>
//         {ranks.map((r) => (
//           <option key={r} value={r}>
//             {r}
//           </option>
//         ))}
//       </select>
//       <select
//         disabled={disabled}
//         value={card.suit}
//         onChange={(e) => setCard({ ...card, suit: e.target.value })}
//       >
//         <option value="">Suit</option>
//         {suits.map((s) => (
//           <option key={s} value={s}>
//             {s}
//           </option>
//         ))}
//       </select>
//     </div>
//   );

//   return (
//     <div className="hole-card-selector">
//       {createCardOptions(card1, setCard1)}
//       {createCardOptions(card2, setCard2)}

//       <div className="selected-preview">
//         Selected:{" "}
//         {[card1, card2].map((c, i) =>
//           c.rank && c.suit ? (
//             <span key={i} className="card-preview">
//               {c.rank + c.suit}
//             </span>
//           ) : (
//             <span key={i}>-- </span>
//           )
//         )}
//       </div>
//     </div>
//   );
    return (
        <div className="hole-card-selector">
        <input
            ref={inputRef}
            type="text"
            maxLength={4}
            value={cardInput}
            onChange={(e) => setCardInput(e.target.value)}
            placeholder="e.g. qhtd"
            disabled={disabled}
            className="card-input"
        />
        </div>
    );
}
