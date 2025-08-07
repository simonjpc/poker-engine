import React, { useEffect, useRef } from "react";
import "./HoleCardSelector.css";


export default function HoleCardSelector({ cardInput, setCardInput, disabled, onSubmit }) {
    const inputRef = useRef(null);
    
    useEffect(() => {
            if (!disabled && inputRef.current) {
            inputRef.current.focus(); // Autofocus when component mounts
            }
        }, [disabled]);

    return (
        <div className="hole-card-selector">
        <input
            ref={inputRef}
            type="text"
            maxLength={4}
            value={cardInput}
            onChange={(e) => setCardInput(e.target.value)}
            onKeyDown={(e) => {
                if (e.key === "Enter") {
                    e.preventDefault();
                    if (onSubmit) onSubmit();  // ⏎ triggers start
                }
            }}
            placeholder="e.g. qhtd"
            disabled={disabled}
            className="card-input"
        />
        </div>
    );
}
