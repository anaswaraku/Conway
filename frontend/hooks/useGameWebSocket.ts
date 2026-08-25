import { useEffect, useRef, useState, useCallback } from "react";
import { GameState, WSClientMessage, WSServerMessage, BoundaryMode } from "../lib/types";

export type ConnectionStatus = "connecting" | "connected" | "disconnected";

export function useGameWebSocket(url: string = "ws://127.0.0.1:8000/ws/game") {
  const [status, setStatus] = useState<ConnectionStatus>("disconnected");
  const [error, setError] = useState<string | null>(null);
  
  // Game state representation
  const [gameState, setGameState] = useState<GameState>({
    generation: 0,
    grid: [],
    live_count: 0,
    is_running: false,
    speed: 10,
    width: 50,
    height: 50,
    boundary_mode: "toroidal",
  });

  const socketRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<number | null>(null);

  const sendMessage = useCallback((msg: WSClientMessage) => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify(msg));
    } else {
      console.warn("WebSocket is not open. Message not sent:", msg);
    }
  }, []);

  const connect = useCallback(() => {
    if (socketRef.current) {
      socketRef.current.close();
    }

    setStatus("connecting");
    setError(null);

    const ws = new WebSocket(url);
    socketRef.current = ws;

    ws.onopen = () => {
      setStatus("connected");
      setError(null);
    };

    ws.onmessage = (event) => {
      try {
        const data: WSServerMessage = JSON.parse(event.data);
        if (data.type === "state_update") {
          setGameState((prev) => ({
            ...prev,
            generation: data.generation,
            grid: data.grid,
            live_count: data.live_count,
            is_running: data.is_running,
            speed: data.speed,
            boundary_mode: data.boundary_mode || prev.boundary_mode,
            // Keep local dimension mapping in sync if server grid size changes
            width: data.grid[0]?.length || prev.width,
            height: data.grid.length || prev.height,
          }));
        } else if (data.type === "error") {
          setError(data.message);
        }
      } catch (err) {
        console.error("Error parsing WebSocket message:", err);
      }
    };

    ws.onerror = () => {
      setError("WebSocket connection error.");
    };

    ws.onclose = () => {
      setStatus("disconnected");
      socketRef.current = null;

      // Attempt automatic reconnect after 3 seconds
      reconnectTimeoutRef.current = window.setTimeout(() => {
        connect();
      }, 3000);
    };
  }, [url]);

  // Connect on mount, cleanup on unmount
  useEffect(() => {
    connect();

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (socketRef.current) {
        // Remove onclose handler to prevent reconnecting on intentional close
        socketRef.current.onclose = null;
        socketRef.current.close();
      }
    };
  }, [connect]);

  // Client command helpers
  const initBoard = useCallback((width: number, height: number, mode: BoundaryMode, initialGrid?: number[][]) => {
    setGameState((prev) => ({ ...prev, width, height, boundary_mode: mode }));
    sendMessage({
      type: "init",
      width,
      height,
      boundary_mode: mode,
      initial_grid: initialGrid,
    });
  }, [sendMessage]);

  const startSimulation = useCallback(() => {
    sendMessage({ type: "start" });
  }, [sendMessage]);

  const pauseSimulation = useCallback(() => {
    sendMessage({ type: "pause" });
  }, [sendMessage]);

  const stepSimulation = useCallback(() => {
    sendMessage({ type: "step" });
  }, [sendMessage]);

  const resetSimulation = useCallback(() => {
    sendMessage({ type: "reset" });
  }, [sendMessage]);

  const setSpeed = useCallback((speed: number) => {
    sendMessage({ type: "set_speed", speed });
  }, [sendMessage]);

  const setCell = useCallback((x: number, y: number, alive: boolean) => {
    // Optimistic local state update for instant draw response
    setGameState((prev) => {
      if (!prev.grid[y]) return prev;
      const newGrid = prev.grid.map((row) => [...row]);
      newGrid[y][x] = alive ? 1 : 0;
      return { ...prev, grid: newGrid };
    });

    sendMessage({ type: "set_cell", x, y, alive });
  }, [sendMessage]);

  const loadPresetPattern = useCallback((patternId: string) => {
    sendMessage({ type: "load_preset", pattern_id: patternId });
  }, [sendMessage]);

  return {
    status,
    error,
    gameState,
    initBoard,
    startSimulation,
    pauseSimulation,
    stepSimulation,
    resetSimulation,
    setSpeed,
    setCell,
    loadPresetPattern,
    reconnect: connect,
  };
}
