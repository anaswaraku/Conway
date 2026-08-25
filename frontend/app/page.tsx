'use client';

import React from 'react';
import { useGameWebSocket } from '../hooks/useGameWebSocket';
import { BoardCanvas } from '../components/BoardCanvas';
import { ControlPanel } from '../components/ControlPanel';

export default function Home() {
  const {
    status,
    error,
    gameState,
    startSimulation,
    pauseSimulation,
    stepSimulation,
    resetSimulation,
  } = useGameWebSocket();

  const isConnected = status === 'connected';

  return (
    <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto', fontFamily: 'sans-serif', textAlign: 'center' }}>
      <h1 className="gradient-text" style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>
        Conway&apos;s Game of Life
      </h1>
      <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem' }}>
        Status: <strong style={{ color: isConnected ? 'var(--accent-cyan)' : 'var(--text-muted)' }}>{status}</strong>
      </p>

      {error && (
        <div style={{ color: 'red', marginBottom: '1rem', padding: '0.5rem', border: '1px solid red', borderRadius: '8px' }}>
          {error}
        </div>
      )}

      {/* Grid Canvas showing the board state from the server */}
      {gameState.grid && gameState.grid.length > 0 ? (
        <BoardCanvas
          grid={gameState.grid}
          width={gameState.width}
          height={gameState.height}
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
    </div>
  );
}
