import React from "react";

interface ControlPanelProps {
  is_running: boolean;
  onStart: () => void;
  onPause: () => void;
  onStep: () => void;
  onReset: () => void;
  isConnected: boolean;
}

export function ControlPanel({
  is_running,
  onStart,
  onPause,
  onStep,
  onReset,
  isConnected,
}: ControlPanelProps) {
  return (
    <div style={{ display: "flex", justifyContent: "center", gap: "0.75rem", margin: "1.5rem 0", flexWrap: "wrap" }}>
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
