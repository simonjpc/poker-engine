import React, { useEffect, useRef } from "react";
import "./HoleCardSelector.css";

export default function TurnCardSelector({ turnInput, setTurnInput, onSubmit, disabled }) {
  const inputRef = useRef(null);

  useEffect(() => {
    if (!disabled && inputRef.current) {
      inputRef.current.focus();
    }
  }, [disabled]);

  return (
    <div className="hole-card-selector">
      <input
        ref={inputRef}
        type="text"
        maxLength={2}
        value={turnInput}
        onChange={(e) => setTurnInput(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            e.preventDefault();
            if (onSubmit) onSubmit();
          }
        }}
        placeholder="e.g. qc"
        disabled={disabled}
        className="card-input"
      />
    </div>
  );
}