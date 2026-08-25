import React from "react";
import { PresetPattern } from "../lib/types";

interface PresetSelectorProps {
  patterns: PresetPattern[];
  onLoadPreset: (patternId: string) => void;
  isConnected: boolean;
}

export function PresetSelector({ patterns, onLoadPreset, isConnected }: PresetSelectorProps) {
  const handleSelect = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const val = event.target.value;
    if (val) {
      onLoadPreset(val);
    }
  };

  return (
    <div style={{ margin: "1rem 0", display: "flex", justifyContent: "center", alignItems: "center", gap: "0.5rem" }}>
      <label htmlFor="preset-select" style={{ fontSize: "0.95rem", color: "var(--text-muted)" }}>
        Load Preset:
      </label>
      <select
        id="preset-select"
        onChange={handleSelect}
        defaultValue=""
        disabled={!isConnected}
        style={{
          padding: "0.5rem 1rem",
          background: "var(--bg-card)",
          border: "1px solid var(--bg-card-border)",
          borderRadius: "8px",
          color: "var(--text-main)",
          fontSize: "0.95rem",
          cursor: isConnected ? "pointer" : "not-allowed",
          outline: "none",
        }}
      >
        <option value="" disabled>
          -- Choose a Preset Pattern --
        </option>
        {patterns.map((pattern) => (
          <option key={pattern.id} value={pattern.id}>
            {pattern.name} ({pattern.category})
          </option>
        ))}
      </select>
    </div>
  );
}
