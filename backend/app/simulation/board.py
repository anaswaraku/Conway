from enum import Enum
from typing import List, Optional, Tuple


class BoundaryMode(str, Enum):
    TOROIDAL = "toroidal"  # Edges wrap around top-bottom and left-right
    BOUNDED = "bounded"    # Cells beyond edges are treated as dead (0)


class Board:
    """
    Represents a 2D Grid for Conway's Game of Life.
    Stores cell state (1 for live, 0 for dead) and provides neighbor calculation logic.
    """

    MIN_SIZE: int = 3
    MAX_SIZE: int = 200

    def __init__(
        self,
        width: int = 50,
        height: int = 50,
        boundary_mode: BoundaryMode = BoundaryMode.TOROIDAL,
        initial_grid: Optional[List[List[int]]] = None,
    ) -> None:
        if not (self.MIN_SIZE <= width <= self.MAX_SIZE):
            raise ValueError(f"Width must be between {self.MIN_SIZE} and {self.MAX_SIZE}")
        if not (self.MIN_SIZE <= height <= self.MAX_SIZE):
            raise ValueError(f"Height must be between {self.MIN_SIZE} and {self.MAX_SIZE}")

        self.width = width
        self.height = height
        self.boundary_mode = boundary_mode

        if initial_grid is not None:
            self._validate_and_set_grid(initial_grid)
        else:
            self.clear()

    def clear(self) -> None:
        """Resets all cells to dead state (0)."""
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]

    def _validate_and_set_grid(self, grid: List[List[int]]) -> None:
        if len(grid) != self.height:
            raise ValueError(f"Grid height {len(grid)} does not match board height {self.height}")
        for row in grid:
            if len(row) != self.width:
                raise ValueError(f"Grid row width {len(row)} does not match board width {self.width}")
            for val in row:
                if val not in (0, 1):
                    raise ValueError(f"Cell value must be 0 or 1, got {val}")

        self.grid = [[val for val in row] for row in grid]

    def get_cell(self, x: int, y: int) -> int:
        """
        Retrieves cell state at (x, y).
        x is column index (0 to width - 1), y is row index (0 to height - 1).
        """
        if self.boundary_mode == BoundaryMode.TOROIDAL:
            norm_x = x % self.width
            norm_y = y % self.height
            return self.grid[norm_y][norm_x]
        else:
            if 0 <= x < self.width and 0 <= y < self.height:
                return self.grid[y][x]
            return 0  # Off-board cells count as dead

    def set_cell(self, x: int, y: int, state: int) -> None:
        """Sets cell state at (x, y) to state (0 or 1)."""
        if state not in (0, 1):
            raise ValueError(f"Cell state must be 0 or 1, got {state}")
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError(f"Coordinates ({x}, {y}) are out of board bounds ({self.width}x{self.height})")
        self.grid[y][x] = state

    def toggle_cell(self, x: int, y: int) -> int:
        """Toggles cell state at (x, y) between 0 and 1. Returns new state."""
        current = self.get_cell(x, y)
        new_state = 1 if current == 0 else 0
        self.set_cell(x, y, new_state)
        return new_state

    def count_live_neighbors(self, x: int, y: int) -> int:
        """Calculates the number of active (1) neighbors surrounding cell (x, y)."""
        count = 0
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                count += self.get_cell(x + dx, y + dy)
        return count

    @property
    def live_cell_count(self) -> int:
        """Returns total number of live cells on the board."""
        return sum(sum(row) for row in self.grid)

    def clone(self) -> "Board":
        """Creates a deep copy of the board."""
        return Board(
            width=self.width,
            height=self.height,
            boundary_mode=self.boundary_mode,
            initial_grid=self.grid,
        )

    def to_dict(self) -> dict:
        """Serializes board state to dictionary."""
        return {
            "width": self.width,
            "height": self.height,
            "boundary_mode": self.boundary_mode.value,
            "grid": self.grid,
            "live_count": self.live_cell_count,
        }
