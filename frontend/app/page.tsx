'use client';

import React, { useEffect, useState } from 'react';
import { useGameWebSocket } from '../hooks/useGameWebSocket';
import { BoardCanvas } from '../components/BoardCanvas';
import { ControlPanel } from '../components/ControlPanel';
import { fetchPresetPatterns } from '../lib/api';
import { PresetPattern } from '../lib/types';

export default function Home() {
  const {
    status,
    error: wsError,
    gameState,
    startSimulation,
    pauseSimulation,
    stepSimulation,
    resetSimulation,
    setCell,
  } = useGameWebSocket();

  // Pattern fetching states
  const [patterns, setPatterns] = useState<PresetPattern[]>([]);
  const [patternsLoading, setPatternsLoading] = useState<boolean>(true);
  const [patternsError, setPatternsError] = useState<string | null>(null);

  useEffect(() => {
    fetchPresetPatterns()
      .then((data) => {
        setPatterns(data);
        setPatternsLoading(false);
      })
      .catch((err) => {
        setPatternsError(err.message || 'Failed to load patterns.');
        setPatternsLoading(false);
      });
  }, []);

  const isConnected = status === 'connected';

  return (
    <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto', fontFamily: 'sans-serif', textAlign: 'center' }}>
      <h1 className="gradient-text" style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>
        Conway&apos;s Game of Life
      </h1>
      <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem' }}>
        Status: <strong style={{ color: isConnected ? 'var(--accent-cyan)' : 'var(--text-muted)' }}>{status}</strong>
      </p>

      {wsError && (
        <div style={{ color: 'red', marginBottom: '1rem', padding: '0.5rem', border: '1px solid red', borderRadius: '8px' }}>
          {wsError}
        </div>
      )}

      {/* Grid Canvas showing the board state from the server */}
      {gameState.grid && gameState.grid.length > 0 ? (
        <BoardCanvas
          grid={gameState.grid}
          width={gameState.width}
          height={gameState.height}
          onCellToggle={setCell}
        />
      ) : (
        <p style={{ color: 'var(--text-muted)' }}>Connecting and loading board state...</p>
      )}

      {/* Basic Simulation Toggles */}
      <ControlPanel
        is_running={gameState.is_running}
        isConnected={isConnected}
        onStart={startSimulation}
        onPause={pauseSimulation}
        onStep={stepSimulation}
        onReset={resetSimulation}
      />

      <div style={{ marginTop: '1.5rem', color: 'var(--text-muted)' }}>
        <p>Generation: {gameState.generation} | Live Cells: {gameState.live_count}</p>
      </div>

      {/* Patterns loading display checklist */}
      <div style={{ marginTop: '2rem', padding: '1rem', border: '1px solid var(--bg-card-border)', borderRadius: '12px' }}>
        <h3>Available Presets Checklist</h3>
        {patternsLoading && <p>Loading patterns...</p>}
        {patternsError && <p style={{ color: 'red' }}>Error loading patterns: {patternsError}</p>}
        {!patternsLoading && !patternsError && (
          <ul style={{ listStyle: 'none', padding: 0, display: 'flex', gap: '0.5rem', justifyContent: 'center', flexWrap: 'wrap', marginTop: '0.5rem' }}>
            {patterns.map((p) => (
              <li key={p.id} style={{ background: '#1e293b', padding: '0.25rem 0.5rem', borderRadius: '6px', fontSize: '0.85rem' }}>
                {p.name} ({p.cell_count} cells)
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
