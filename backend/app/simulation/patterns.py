from typing import Dict, List, Tuple, Any, Optional
from app.simulation.board import Board


# Preset Patterns represented by relative (dx, dy) coordinate offsets from center/top-left
PATTERNS: Dict[str, Dict[str, Any]] = {
    "block": {
        "name": "Block",
        "category": "Still Life",
        "description": "2x2 static square pattern.",
        "cells": [(0, 0), (1, 0), (0, 1), (1, 1)],
    },
    "beehive": {
        "name": "Beehive",
        "category": "Still Life",
        "description": "Hexagonal 6-cell static pattern.",
        "cells": [(1, 0), (2, 0), (0, 1), (3, 1), (1, 2), (2, 2)],
    },
    "blinker": {
        "name": "Blinker",
        "category": "Oscillator",
        "description": "3-cell period-2 oscillator.",
        "cells": [(0, 0), (1, 0), (2, 0)],
    },
    "toad": {
        "name": "Toad",
        "category": "Oscillator",
        "description": "6-cell period-2 oscillator.",
        "cells": [(1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1)],
    },
    "beacon": {
        "name": "Beacon",
        "category": "Oscillator",
        "description": "8-cell period-2 oscillator.",
        "cells": [(0, 0), (1, 0), (0, 1), (1, 1), (2, 2), (3, 2), (2, 3), (3, 3)],
    },
    "glider": {
        "name": "Glider",
        "category": "Spaceship",
        "description": "Smallest spaceship that travels diagonally across the grid.",
        "cells": [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)],
    },
    "pulsar": {
        "name": "Pulsar",
        "category": "Oscillator",
        "description": "Large period-3 oscillator.",
        "cells": [
            # Top-left quadrant
            (-4, -6), (-3, -6), (-2, -6), (-6, -4), (-6, -3), (-6, -2),
            (-1, -4), (-1, -3), (-1, -2), (-4, -1), (-3, -1), (-2, -1),
            # Top-right quadrant
            (2, -6), (3, -6), (4, -6), (6, -4), (6, -3), (6, -2),
            (1, -4), (1, -3), (1, -2), (2, -1), (3, -1), (4, -1),
            # Bottom-left quadrant
            (-4, 6), (-3, 6), (-2, 6), (-6, 4), (-6, 3), (-6, 2),
            (-1, 4), (-1, 3), (-1, 2), (-4, 1), (-3, 1), (-2, 1),
            # Bottom-right quadrant
            (2, 6), (3, 6), (4, 6), (6, 4), (6, 3), (6, 2),
            (1, 4), (1, 3), (1, 2), (2, 1), (3, 1), (4, 1),
        ],
    },
    "gosper_glider_gun": {
        "name": "Gosper Glider Gun",
        "category": "Gun",
        "description": "First known gun pattern that creates endless gliders.",
        "cells": [
            (24, 0),
            (22, 1), (24, 1),
            (12, 2), (13, 2), (20, 2), (21, 2), (34, 2), (35, 2),
            (11, 3), (15, 3), (20, 3), (21, 3), (34, 3), (35, 3),
            (0, 4), (1, 4), (10, 4), (16, 4), (20, 4), (21, 4),
            (0, 5), (1, 5), (10, 5), (14, 5), (16, 5), (17, 5), (22, 5), (24, 5),
            (10, 6), (16, 6), (24, 6),
            (11, 7), (15, 7),
            (12, 8), (13, 8),
        ],
    },
}


def get_available_presets() -> List[Dict[str, Any]]:
    """Returns metadata list of all available preset patterns."""
    return [
        {
            "id": key,
            "name": meta["name"],
            "category": meta["category"],
            "description": meta["description"],
            "cell_count": len(meta["cells"]),
        }
        for key, meta in PATTERNS.items()
    ]


def load_preset(board: Board, pattern_key: str, offset_x: Optional[int] = None, offset_y: Optional[int] = None) -> Board:
    """
    Loads a preset pattern onto the given board.
    By default, centers the pattern on the board unless custom offsets are provided.
    """
    if pattern_key not in PATTERNS:
        raise ValueError(f"Unknown pattern key '{pattern_key}'. Available: {list(PATTERNS.keys())}")

    pattern = PATTERNS[pattern_key]
    cells = pattern["cells"]

    board.clear()

    # Calculate bounding box of pattern to center it properly
    min_x = min(c[0] for c in cells)
    max_x = max(c[0] for c in cells)
    min_y = min(c[1] for c in cells)
    max_y = max(c[1] for c in cells)

    pattern_width = max_x - min_x + 1
    pattern_height = max_y - min_y + 1

    if offset_x is None:
        start_x = (board.width - pattern_width) // 2 - min_x
    else:
        start_x = offset_x

    if offset_y is None:
        start_y = (board.height - pattern_height) // 2 - min_y
    else:
        start_y = offset_y

    for dx, dy in cells:
        target_x = start_x + dx
        target_y = start_y + dy
        if 0 <= target_x < board.width and 0 <= target_y < board.height:
            board.set_cell(target_x, target_y, 1)

    return board
