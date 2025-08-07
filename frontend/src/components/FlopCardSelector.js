import React, { useEffect, useRef } from "react";
import "./HoleCardSelector.css";

export default function FlopCardSelector({ flopInput, setFlopInput, onSubmit, disabled }) {
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
        maxLength={6}
        value={flopInput}
        onChange={(e) => setFlopInput(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            e.preventDefault();
            if (onSubmit) onSubmit();
          }
        }}
        placeholder="e.g. 8s9hjd"
        disabled={disabled}
        className="card-input"
      />
    </div>
  );
}