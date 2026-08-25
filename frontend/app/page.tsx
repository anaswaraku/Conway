'use client';

import React from 'react';

export default function Home() {
  return (
    <div style={{ padding: '2rem', textAlign: 'center' }}>
      <h1 className="gradient-text" style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>
        Conway&apos;s Game of Life
      </h1>
      <p style={{ color: 'var(--text-muted)' }}>
        Full-Stack Realtime Simulation Engine
      </p>
    </div>
  );
}
