import React from "react";
import { BoundaryMode } from "../lib/types";

interface ControlPanelProps {
  is_running: boolean;
  onStart: () => void;
  onPause: () => void;
  onStep: () => void;
  onReset: () => void;
  isConnected: boolean;
  speed: number;
  onSpeedChange: (speed: number) => void;
  boundaryMode: BoundaryMode;
  onBoundaryModeChange: (mode: BoundaryMode) => void;
}

export function ControlPanel({
  is_running,
  onStart,
  onPause,
  onStep,
  onReset,
  isConnected,
  speed,
  onSpeedChange,
  boundaryMode,
  onBoundaryModeChange,
}: ControlPanelProps) {
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "1.25rem", margin: "1.5rem 0" }}>
      {/* Primary Action Buttons */}
      <div style={{ display: "flex", justifyContent: "center", gap: "0.75rem", flexWrap: "wrap" }}>
        <button
          onClick={onStart}
          disabled={!isConnected || is_running}
          style={{ ...btnStyle, backgroundColor: is_running ? "#1e293b" : "#10b981" }}
        >
          Start
        </button>
        <button
          onClick={onPause}
          disabled={!isConnected || !is_running}
          style={{ ...btnStyle, backgroundColor: !is_running ? "#1e293b" : "#f59e0b" }}
        >
          Pause
        </button>
        <button
          onClick={onStep}
          disabled={!isConnected || is_running}
          style={{ ...btnStyle, backgroundColor: is_running ? "#1e293b" : "#3b82f6" }}
        >
          Step
        </button>
        <button
          onClick={onReset}
          disabled={!isConnected}
          style={{ ...btnStyle, backgroundColor: "#ef4444" }}
        >
          Reset
        </button>
      </div>

      {/* Simulation Controls: Speed Slider & Boundary Mode */}
      <div style={{ display: "flex", justifyContent: "center", alignItems: "center", gap: "2rem", flexWrap: "wrap", width: "100%", maxWidth: "600px" }}>
        {/* Speed Slider */}
        <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
          <label htmlFor="speed-slider" style={{ fontSize: "0.9rem", color: "var(--text-muted)", minWidth: "90px" }}>
            Speed: <strong>{speed} Hz</strong>
          </label>
          <input
            id="speed-slider"
            type="range"
            min="1"
            max="30"
            value={speed}
            disabled={!isConnected}
            onChange={(e) => onSpeedChange(Number(e.target.value))}
            style={{ cursor: isConnected ? "pointer" : "not-allowed", accentColor: "var(--accent-cyan)" }}
          />
        </div>

        {/* Boundary Mode Select */}
        <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
          <label htmlFor="boundary-select" style={{ fontSize: "0.9rem", color: "var(--text-muted)" }}>
            Boundary:
          </label>
          <select
            id="boundary-select"
            value={boundaryMode}
            disabled={!isConnected}
            onChange={(e) => onBoundaryModeChange(e.target.value as BoundaryMode)}
            style={{
              padding: "0.4rem 0.8rem",
              background: "var(--bg-card)",
              border: "1px solid var(--bg-card-border)",
              borderRadius: "8px",
              color: "var(--text-main)",
              fontSize: "0.85rem",
              cursor: isConnected ? "pointer" : "not-allowed",
              outline: "none",
            }}
          >
            <option value="toroidal">Toroidal (Wrap)</option>
            <option value="bounded">Bounded (Edges Dead)</option>
          </select>
        </div>
      </div>
    </div>
  );
}

const btnStyle: React.CSSProperties = {
  padding: "0.6rem 1.2rem",
  color: "#ffffff",
  border: "none",
  borderRadius: "8px",
  cursor: "pointer",
  fontWeight: "bold",
  fontSize: "0.95rem",
  transition: "all 0.2s ease",
  minWidth: "80px",
  boxShadow: "0 2px 8px rgba(0, 0, 0, 0.2)",
};
