from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from app.simulation.board import BoundaryMode, Board


class BoardConfig(BaseModel):
    width: int = Field(50, ge=Board.MIN_SIZE, le=Board.MAX_SIZE, description="Board width")
    height: int = Field(50, ge=Board.MIN_SIZE, le=Board.MAX_SIZE, description="Board height")
    boundary_mode: BoundaryMode = Field(BoundaryMode.TOROIDAL, description="Edge boundary wrapping mode")
    initial_grid: Optional[List[List[int]]] = Field(None, description="Optional custom initial grid of 0s and 1s")

    @field_validator("initial_grid")
    @classmethod
    def validate_grid_values(cls, v: Optional[List[List[int]]]) -> Optional[List[List[int]]]:
        if v is None:
            return v
        for row in v:
            for val in row:
                if val not in (0, 1):
                    raise ValueError("Cell values in the initial_grid must be either 0 or 1.")
        return v


class BoardStateResponse(BaseModel):
    width: int
    height: int
    boundary_mode: str
    grid: List[List[int]]
    live_count: int


class PresetPatternResponse(BaseModel):
    id: str
    name: str
    category: str
    description: str
    cell_count: int


class LoadPresetRequest(BaseModel):
    width: int = Field(50, ge=Board.MIN_SIZE, le=Board.MAX_SIZE)
    height: int = Field(50, ge=Board.MIN_SIZE, le=Board.MAX_SIZE)
    boundary_mode: BoundaryMode = Field(BoundaryMode.TOROIDAL)
    pattern_id: str


class WSClientMessage(BaseModel):
    type: str
    width: Optional[int] = Field(None, ge=Board.MIN_SIZE, le=Board.MAX_SIZE)
    height: Optional[int] = Field(None, ge=Board.MIN_SIZE, le=Board.MAX_SIZE)
    boundary_mode: Optional[BoundaryMode] = None
    initial_grid: Optional[List[List[int]]] = None
    speed: Optional[int] = Field(None, ge=1, le=30)
    x: Optional[int] = None
    y: Optional[int] = None
    alive: Optional[bool] = None
    pattern_id: Optional[str] = None

