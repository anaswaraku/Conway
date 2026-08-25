import asyncio
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import ValidationError
from app.schemas.game import WSClientMessage
from app.simulation.board import Board
from app.simulation.engine import Engine
from app.simulation.patterns import load_preset

router = APIRouter()
logger = logging.getLogger("websocket")


@router.websocket("/ws/game")
async def websocket_game_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Initialize simulation components
    board = Board(width=50, height=50)
    engine = Engine(board)
    speed = 10  # ticks/seconds
    ticker_task = None

    async def send_state():
        state = engine.to_dict()
        await websocket.send_json({
            "type": "state_update",
            "generation": state["generation"],
            "grid": state["board"]["grid"],
            "live_count": state["live_count"],
            "is_running": engine.is_running,
            "speed": speed,
        })

    async def ticker_loop():
        nonlocal speed
        try:
            while True:
                if engine.is_running:
                    engine.tick()
                    await send_state()
                # Dynamically sleep based on speed
                await asyncio.sleep(1.0 / max(1, speed))
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Error in simulation ticker loop: {e}")

    try:
        # Send initial default board state
        await send_state()

        # Start background ticker task
        ticker_task = asyncio.create_task(ticker_loop())

        while True:
            data = await websocket.receive_json()
            try:
                msg = WSClientMessage(**data)
            except ValidationError as e:
                await websocket.send_json({
                    "type": "error",
                    "message": f"Validation Error: {e.errors()}"
                })
                continue

            if msg.type == "init":
                # Pause ticker while modifying configuration
                engine.pause()
                w = msg.width if msg.width is not None else board.width
                h = msg.height if msg.height is not None else board.height
                mode = msg.boundary_mode if msg.boundary_mode is not None else board.boundary_mode
                grid = msg.initial_grid

                try:
                    if grid is not None:
                        if len(grid) != h:
                            raise ValueError(f"Grid height {len(grid)} does not match board height {h}")
                        for row in grid:
                            if len(row) != w:
                                raise ValueError(f"Row width {len(row)} does not match board width {w}")

                    board = Board(width=w, height=h, boundary_mode=mode, initial_grid=grid)
                    engine.set_board(board)
                    await send_state()
                except ValueError as e:
                    await websocket.send_json({"type": "error", "message": str(e)})

            elif msg.type == "start":
                engine.start()
                await send_state()

            elif msg.type == "pause":
                engine.pause()
                await send_state()

            elif msg.type == "step":
                # Single step only allowed when paused or stopped
                engine.pause()
                engine.tick()
                await send_state()

            elif msg.type == "reset":
                engine.reset()
                await send_state()

            elif msg.type == "set_speed":
                if msg.speed is not None:
                    speed = msg.speed
                    await send_state()

            elif msg.type == "set_cell":
                if msg.x is not None and msg.y is not None and msg.alive is not None:
                    try:
                        # set_cell requires valid 0 or 1 value
                        board.set_cell(msg.x, msg.y, 1 if msg.alive else 0)
                        await send_state()
                    except ValueError as e:
                        await websocket.send_json({"type": "error", "message": str(e)})

            elif msg.type == "load_preset":
                if msg.pattern_id is not None:
                    try:
                        engine.pause()
                        load_preset(board, msg.pattern_id)
                        engine.generation = 0
                        await send_state()
                    except ValueError as e:
                        await websocket.send_json({"type": "error", "message": str(e)})
            else:
                await websocket.send_json({
                    "type": "error",
                    "message": f"Unknown command type: {msg.type}"
                })

    except WebSocketDisconnect:
        pass
    finally:
        # Clean up background tick task
        if ticker_task:
            ticker_task.cancel()
            try:
                await ticker_task
            except asyncio.CancelledError:
                pass
