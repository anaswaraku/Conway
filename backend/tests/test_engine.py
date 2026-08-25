import pytest
from app.simulation.board import Board, BoundaryMode
from app.simulation.engine import Engine, SimulationState


def test_empty_board_remains_empty():
    engine = Engine(Board(width=5, height=5))
    engine.tick()
    assert engine.generation == 1
    assert engine.board.live_cell_count == 0


def test_single_live_cell_dies():
    # Rule 1: Underpopulation (< 2 neighbors)
    board = Board(width=5, height=5)
    board.set_cell(2, 2, 1)
    engine = Engine(board)
    engine.tick()
    assert engine.board.get_cell(2, 2) == 0
    assert engine.board.live_cell_count == 0


def test_still_life_block():
    # 2x2 Block still life should remain unchanged indefinitely
    # 1 1
    # 1 1
    board = Board(width=5, height=5)
    board.set_cell(1, 1, 1)
    board.set_cell(1, 2, 1)
    board.set_cell(2, 1, 1)
    board.set_cell(2, 2, 1)

    engine = Engine(board)
    engine.tick()
    assert engine.board.live_cell_count == 4
    assert engine.board.get_cell(1, 1) == 1
    assert engine.board.get_cell(1, 2) == 1
    assert engine.board.get_cell(2, 1) == 1
    assert engine.board.get_cell(2, 2) == 1


def test_oscillator_blinker():
    # Blinker oscillator (period 2)
    # Horizontal: (1,2), (2,2), (3,2)
    # Becomes Vertical: (2,1), (2,2), (2,3)
    board = Board(width=5, height=5)
    board.set_cell(1, 2, 1)
    board.set_cell(2, 2, 1)
    board.set_cell(3, 2, 1)

    engine = Engine(board)

    # Gen 1: Vertical
    engine.tick()
    assert engine.board.get_cell(2, 1) == 1
    assert engine.board.get_cell(2, 2) == 1
    assert engine.board.get_cell(2, 3) == 1
    assert engine.board.get_cell(1, 2) == 0

    # Gen 2: Horizontal again
    engine.tick()
    assert engine.board.get_cell(1, 2) == 1
    assert engine.board.get_cell(2, 2) == 1
    assert engine.board.get_cell(3, 2) == 1
    assert engine.board.get_cell(2, 1) == 0


def test_reproduction_dead_cell_with_three_neighbors():
    # Rule 4: Dead cell with exactly 3 neighbors becomes alive
    board = Board(width=5, height=5)
    board.set_cell(1, 1, 1)
    board.set_cell(1, 2, 1)
    board.set_cell(2, 1, 1)

    # Cell at (2, 2) is dead and has 3 live neighbors: (1,1), (1,2), (2,1)
    assert board.get_cell(2, 2) == 0
    engine = Engine(board)
    engine.tick()
    assert engine.board.get_cell(2, 2) == 1


def test_engine_state_transitions():
    engine = Engine()
    assert engine.state == SimulationState.STOPPED
    assert not engine.is_running

    engine.start()
    assert engine.state == SimulationState.RUNNING
    assert engine.is_running

    engine.pause()
    assert engine.state == SimulationState.PAUSED

    engine.reset()
    assert engine.state == SimulationState.STOPPED
    assert engine.generation == 0
