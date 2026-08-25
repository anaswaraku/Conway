from typing import List
from fastapi import APIRouter, HTTPException, status
from app.schemas.game import BoardConfig, BoardStateResponse, PresetPatternResponse, LoadPresetRequest
from app.simulation.board import Board
from app.simulation.patterns import get_available_presets, load_preset

router = APIRouter(prefix="/api")


@router.get("/patterns", response_model=List[PresetPatternResponse])
def list_patterns():
    """Retrieve all available pattern presets."""
    return get_available_presets()


@router.post("/board/init", response_model=BoardStateResponse)
def initialize_board(config: BoardConfig):
    """
    Initializes a new Game of Life board state.
    Validates optional custom initial_grid size properties.
    """
    try:
        # If grid is provided, perform size mismatch checks
        if config.initial_grid is not None:
            if len(config.initial_grid) != config.height:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail=f"Initial grid height ({len(config.initial_grid)}) does not match config height ({config.height})"
                )
            for row in config.initial_grid:
                if len(row) != config.width:
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                        detail=f"Initial grid row width ({len(row)}) does not match config width ({config.width})"
                    )

        board = Board(
            width=config.width,
            height=config.height,
            boundary_mode=config.boundary_mode,
            initial_grid=config.initial_grid
        )
        return board.to_dict()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_420_METHOD_FAILURE,
            detail=str(e)
        )


@router.post("/board/preset", response_model=BoardStateResponse)
def load_pattern_preset(req: LoadPresetRequest):
    """
    Creates a board and centers the selected preset pattern on it.
    """
    try:
        board = Board(width=req.width, height=req.height, boundary_mode=req.boundary_mode)
        load_preset(board, req.pattern_id)
        return board.to_dict()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
