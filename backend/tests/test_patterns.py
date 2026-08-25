import pytest
from app.simulation.board import Board
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


def test_load_invalid_preset():
    board = Board(width=10, height=10)
    with pytest.raises(ValueError):
        load_preset(board, "non_existent_pattern")
