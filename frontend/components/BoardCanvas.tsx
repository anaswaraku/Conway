import React, { useRef, useEffect } from "react";

interface BoardCanvasProps {
  grid: number[][];
  width: number;
  height: number;
  cellSize?: number;
  onCellToggle?: (x: number, y: number, alive: boolean) => void;
}

export function BoardCanvas({ grid, width, height, cellSize = 12, onCellToggle }: BoardCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const isDrawingRef = useRef<boolean>(false);
  const drawValueRef = useRef<boolean>(true); // true to draw alive, false to erase
  const lastCellRef = useRef<{ x: number; y: number } | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const canvasWidth = width * cellSize;
    const canvasHeight = height * cellSize;

    canvas.width = canvasWidth;
    canvas.height = canvasHeight;

    ctx.clearRect(0, 0, canvasWidth, canvasHeight);

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

    for (let x = 0; x <= width; x++) {
      ctx.beginPath();
      ctx.moveTo(x * cellSize, 0);
      ctx.lineTo(x * cellSize, canvasHeight);
      ctx.stroke();
    }

    for (let y = 0; y <= height; y++) {
      ctx.beginPath();
      ctx.moveTo(0, y * cellSize);
      ctx.lineTo(canvasWidth, y * cellSize);
      ctx.stroke();
    }
  }, [grid, width, height, cellSize]);

  const handleCellAction = (event: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas || !onCellToggle) return;

    const rect = canvas.getBoundingClientRect();
    const clientX = event.clientX - rect.left;
    const clientY = event.clientY - rect.top;

    const cellX = Math.floor(clientX / cellSize);
    const cellY = Math.floor(clientY / cellSize);

    // Validate bounds
    if (cellX >= 0 && cellX < width && cellY >= 0 && cellY < height) {
      // Avoid duplicate trigger on same cell in same drag move
      if (lastCellRef.current?.x === cellX && lastCellRef.current?.y === cellY) {
        return;
      }
      lastCellRef.current = { x: cellX, y: cellY };

      if (event.type === "mousedown") {
        isDrawingRef.current = true;
        // If cell is dead (0), we draw alive (true). If cell is alive (1), we draw dead (false).
        const isCurrentlyAlive = grid[cellY]?.[cellX] === 1;
        drawValueRef.current = !isCurrentlyAlive;
        onCellToggle(cellX, cellY, drawValueRef.current);
      } else if (event.type === "mousemove" && isDrawingRef.current) {
        onCellToggle(cellX, cellY, drawValueRef.current);
      }
    }
  };

  const handleMouseUpOrLeave = () => {
    isDrawingRef.current = false;
    lastCellRef.current = null;
  };

  return (
    <div style={{ overflow: "auto", display: "flex", justifyContent: "center", padding: "1rem" }}>
      <canvas
        ref={canvasRef}
        onMouseDown={handleCellAction}
        onMouseMove={handleCellAction}
        onMouseUp={handleMouseUpOrLeave}
        onMouseLeave={handleMouseUpOrLeave}
        style={{
          border: "1px solid var(--bg-card-border)",
          borderRadius: "8px",
          boxShadow: "0 4px 20px rgba(0, 0, 0, 0.5)",
          cursor: "crosshair",
        }}
      />
    </div>
  );
}
