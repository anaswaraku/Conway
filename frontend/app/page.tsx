'use client';

import React from 'react';
import { useGameWebSocket } from '../hooks/useGameWebSocket';

export default function Home() {
  const {
    status,
    error,
    gameState,
    startSimulation,
    pauseSimulation,
    stepSimulation,
    resetSimulation,
    loadPresetPattern,
  } = useGameWebSocket();

  return (
    <div style={{ padding: '2rem', maxWidth: '600px', margin: '0 auto', fontFamily: 'sans-serif' }}>
      <h1 className="gradient-text" style={{ fontSize: '2rem', marginBottom: '1rem' }}>
        Game of Life Dev Tester
      </h1>

      <div className="glass-panel" style={{ padding: '1.5rem', marginBottom: '1.5rem' }}>
        <p><strong>Connection Status:</strong> {status}</p>
        {error && <p style={{ color: 'red' }}><strong>Error:</strong> {error}</p>}
        <p><strong>Generation:</strong> {gameState.generation}</p>
        <p><strong>Live Cells:</strong> {gameState.live_count}</p>
        <p><strong>Running:</strong> {gameState.is_running ? 'Yes' : 'No'}</p>
        <p><strong>Speed:</strong> {gameState.speed} ticks/sec</p>
      </div>

      <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
        <button onClick={startSimulation} disabled={status !== 'connected'} style={btnStyle}>Start</button>
        <button onClick={pauseSimulation} disabled={status !== 'connected'} style={btnStyle}>Pause</button>
        <button onClick={stepSimulation} disabled={status !== 'connected'} style={btnStyle}>Step</button>
        <button onClick={resetSimulation} disabled={status !== 'connected'} style={btnStyle}>Reset</button>
        <button onClick={() => loadPresetPattern('glider')} disabled={status !== 'connected'} style={btnStyle}>Load Glider</button>
      </div>

      <p style={{ marginTop: '2rem', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
        Open the browser console (F12) to monitor WebSocket messages.
      </p>
    </div>
  );
}

const btnStyle = {
  padding: '0.5rem 1rem',
  background: '#4facfe',
  color: 'white',
  border: 'none',
  borderRadius: '8px',
  cursor: 'pointer',
  fontWeight: 'bold',
};
