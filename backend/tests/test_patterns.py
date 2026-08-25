import pytest
from app.simulation.board import Board
from app.simulation.engine import Engine
from app.simulation.patterns import PATTERNS, get_available_presets, load_preset


def test_get_available_presets():
    presets = get_available_presets()
    assert len(presets) == len(PATTERNS)
    preset_ids = [p["id"] for p in presets]
    assert "glider" in preset_ids
    assert "blinker" in preset_ids
    assert "gosper_glider_gun" in preset_ids


def test_load_preset_glider():
    board = Board(width=20, height=20)
    load_preset(board, "glider")
    assert board.live_cell_count == 5


def test_glider_multigenerational_movement():
    # Glider moves 1 cell diagonally down-right every 4 generations
    board = Board(width=20, height=20)
    load_preset(board, "glider", offset_x=2, offset_y=2)
    engine = Engine(board)

    # Initial live cell positions
    initial_live_cells = set()
    for y in range(20):
        for x in range(20):
            if board.get_cell(x, y) == 1:
                initial_live_cells.add((x, y))

    # Advance 4 generations
    for _ in range(4):
        engine.tick()

    assert engine.generation == 4
    assert board.live_cell_count == 5

    # After 4 generations, each coordinate shifts (+1, +1)
    shifted_live_cells = set()
    for y in range(20):
        for x in range(20):
            if board.get_cell(x, y) == 1:
                shifted_live_cells.add((x, y))

    expected_shifted = {(x + 1, y + 1) for x, y in initial_live_cells}
    assert shifted_live_cells == expected_shifted


def test_load_invalid_preset():
    board = Board(width=10, height=10)
    with pytest.raises(ValueError):
        load_preset(board, "non_existent_pattern")
