import pytest
from app.simulation.board import Board, BoundaryMode


def test_board_initialization():
    board = Board(width=10, height=10)
    assert board.width == 10
    assert board.height == 10
    assert board.live_cell_count == 0
    assert board.boundary_mode == BoundaryMode.TOROIDAL


def test_invalid_board_dimensions():
    with pytest.raises(ValueError):
        Board(width=2, height=10)
    with pytest.raises(ValueError):
        Board(width=10, height=250)


def test_set_get_cell():
    board = Board(width=5, height=5)
    board.set_cell(2, 3, 1)
    assert board.get_cell(2, 3) == 1
    assert board.get_cell(0, 0) == 0

    board.toggle_cell(2, 3)
    assert board.get_cell(2, 3) == 0


def test_toroidal_boundary_neighbors():
    # 5x5 board, set cell at (0, 0)
    board = Board(width=5, height=5, boundary_mode=BoundaryMode.TOROIDAL)
    board.set_cell(0, 0, 1)

    # Wrap-around neighbors of (0,0) include (4,4), (4,0), (4,1), (0,4), (1,4) etc.
    assert board.get_cell(5, 5) == 1  # 5 % 5 = 0, 5 % 5 = 0
    assert board.count_live_neighbors(4, 4) == 1
    assert board.count_live_neighbors(1, 1) == 1


def test_bounded_boundary_neighbors():
    board = Board(width=5, height=5, boundary_mode=BoundaryMode.BOUNDED)
    board.set_cell(0, 0, 1)

    # In bounded mode, off-grid cells return 0
    assert board.get_cell(-1, -1) == 0
    assert board.count_live_neighbors(1, 1) == 1
    assert board.count_live_neighbors(4, 4) == 0  # No wrapping
