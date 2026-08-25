import React, { useRef, useEffect } from "react";

interface BoardCanvasProps {
  grid: number[][];
  width: number;
  height: number;
  cellSize?: number;
}

export function BoardCanvas({ grid, width, height, cellSize = 12 }: BoardCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Calculate canvas size based on cells and dimensions
    const canvasWidth = width * cellSize;
    const canvasHeight = height * cellSize;

    canvas.width = canvasWidth;
    canvas.height = canvasHeight;

    // Clear canvas
    ctx.clearRect(0, 0, canvasWidth, canvasHeight);

    // Get styling values from theme CSS variables (fall back to defaults if not loaded)
    const aliveColor = getComputedStyle(document.documentElement).getPropertyValue("--cell-alive").trim() || "#00f2fe";
    const deadColor = getComputedStyle(document.documentElement).getPropertyValue("--cell-dead").trim() || "#111827";
    const gridColor = getComputedStyle(document.documentElement).getPropertyValue("--grid-line").trim() || "rgba(255, 255, 255, 0.04)";

    // 1. Draw cells
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        const isAlive = grid[y]?.[x] === 1;
        ctx.fillStyle = isAlive ? aliveColor : deadColor;
        ctx.fillRect(x * cellSize, y * cellSize, cellSize, cellSize);
      }
    }

    // 2. Draw grid lines
    ctx.strokeStyle = gridColor;
    ctx.lineWidth = 0.5;

    // Vertical lines
    for (let x = 0; x <= width; x++) {
      ctx.beginPath();
      ctx.moveTo(x * cellSize, 0);
      ctx.lineTo(x * cellSize, canvasHeight);
      ctx.stroke();
    }

    // Horizontal lines
    for (let y = 0; y <= height; y++) {
      ctx.beginPath();
      ctx.moveTo(0, y * cellSize);
      ctx.lineTo(canvasWidth, y * cellSize);
      ctx.stroke();
    }
  }, [grid, width, height, cellSize]);

  return (
    <div style={{ overflow: "auto", display: "flex", justifyContent: "center", padding: "1rem" }}>
      <canvas
        ref={canvasRef}
        style={{
          border: "1px solid var(--bg-card-border)",
          borderRadius: "8px",
          boxShadow: "0 4px 20px rgba(0, 0, 0, 0.5)",
        }}
      />
    </div>
  );
}
