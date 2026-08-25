from enum import Enum
from typing import Dict, Optional, Any
from app.simulation.board import Board


class SimulationState(str, Enum):
    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"


class Engine:
    """
    Independent Conway's Game of Life Simulation Engine.
    Processes generation state transitions based on standard Conway rules:
    1. Live cell with < 2 live neighbors -> Dies (Underpopulation)
    2. Live cell with 2 or 3 live neighbors -> Survives
    3. Live cell with > 3 live neighbors -> Dies (Overpopulation)
    4. Dead cell with == 3 live neighbors -> Becomes alive (Reproduction)
    """

    def __init__(self, board: Optional[Board] = None) -> None:
        self.board = board if board is not None else Board()
        self.generation: int = 0
        self.state: SimulationState = SimulationState.STOPPED

    def set_board(self, board: Board) -> None:
        """Assigns a new board and resets generation state."""
        self.board = board
        self.generation = 0

    def tick(self) -> Board:
        """
        Advances the simulation by exactly one generation.
        Returns the updated Board instance.
        """
        new_grid = [[0 for _ in range(self.board.width)] for _ in range(self.board.height)]

        for y in range(self.board.height):
            for x in range(self.board.width):
                current_state = self.board.get_cell(x, y)
                live_neighbors = self.board.count_live_neighbors(x, y)

                if current_state == 1:
                    # Rule 1 & 3: Dies under 2 or over 3 live neighbors
                    # Rule 2: Survives with 2 or 3 live neighbors
                    if live_neighbors in (2, 3):
                        new_grid[y][x] = 1
                    else:
                        new_grid[y][x] = 0
                else:
                    # Rule 4: Dead cell with exactly 3 live neighbors becomes alive
                    if live_neighbors == 3:
                        new_grid[y][x] = 1

        self.board.grid = new_grid
        self.generation += 1
        return self.board

    def start(self) -> None:
        """Sets simulation state to RUNNING."""
        self.state = SimulationState.RUNNING

    def pause(self) -> None:
        """Sets simulation state to PAUSED."""
        self.state = SimulationState.PAUSED

    def reset(self) -> None:
        """Clears board cells and resets generation counter to 0."""
        self.board.clear()
        self.generation = 0
        self.state = SimulationState.STOPPED

    @property
    def is_running(self) -> bool:
        return self.state == SimulationState.RUNNING

    def to_dict(self) -> Dict[str, Any]:
        """Serializes current engine state to a dictionary."""
        return {
            "generation": self.generation,
            "state": self.state.value,
            "is_running": self.is_running,
            "live_count": self.board.live_cell_count,
            "board": self.board.to_dict(),
        }
