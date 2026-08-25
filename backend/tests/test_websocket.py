import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_websocket_connection_and_initial_state():
    with client.websocket_connect("/ws/game") as websocket:
        # The websocket sends initial state update upon connection
        data = websocket.receive_json()
        assert data["type"] == "state_update"
        assert data["generation"] == 0
        assert data["is_running"] is False
        assert len(data["grid"]) == 50
        assert len(data["grid"][0]) == 50
        assert data["speed"] == 10


def test_websocket_commands():
    with client.websocket_connect("/ws/game") as websocket:
        # Discard initial state
        websocket.receive_json()

        # Command: start
        websocket.send_json({"type": "start"})
        data = websocket.receive_json()
        assert data["type"] == "state_update"
        assert data["is_running"] is True

        # Command: pause
        websocket.send_json({"type": "pause"})
        data = websocket.receive_json()
        assert data["type"] == "state_update"
        assert data["is_running"] is False

        # Command: step
        websocket.send_json({"type": "step"})
        data = websocket.receive_json()
        assert data["type"] == "state_update"
        assert data["generation"] == 1
        assert data["is_running"] is False

        # Command: set_speed
        websocket.send_json({"type": "set_speed", "speed": 15})
        data = websocket.receive_json()
        assert data["type"] == "state_update"
        assert data["speed"] == 15

        # Command: reset
        websocket.send_json({"type": "reset"})
        data = websocket.receive_json()
        assert data["type"] == "state_update"
        assert data["generation"] == 0
        assert data["live_count"] == 0


def test_websocket_set_cell_interactive():
    with client.websocket_connect("/ws/game") as websocket:
        websocket.receive_json()  # discard initial

        # Command: set_cell at (10, 15) to alive
        websocket.send_json({"type": "set_cell", "x": 10, "y": 15, "alive": True})
        data = websocket.receive_json()
        assert data["type"] == "state_update"
        assert data["grid"][15][10] == 1
        assert data["live_count"] == 1

        # Command: set_cell to dead
        websocket.send_json({"type": "set_cell", "x": 10, "y": 15, "alive": False})
        data = websocket.receive_json()
        assert data["type"] == "state_update"
        assert data["grid"][15][10] == 0
        assert data["live_count"] == 0


def test_websocket_load_preset():
    with client.websocket_connect("/ws/game") as websocket:
        websocket.receive_json()  # discard initial

        # Start simulation
        websocket.send_json({"type": "start"})
        websocket.receive_json()

        # Command: load glider (should pause the simulation)
        websocket.send_json({"type": "load_preset", "pattern_id": "glider"})
        data = websocket.receive_json()
        assert data["type"] == "state_update"
        assert data["live_count"] == 5
        assert data["generation"] == 0
        assert data["is_running"] is False


def test_websocket_init_custom_board():
    with client.websocket_connect("/ws/game") as websocket:
        websocket.receive_json()  # discard initial

        # Command: init board to 10x10 with custom grid
        custom_grid = [[0] * 10 for _ in range(10)]
        custom_grid[1][2] = 1
        custom_grid[2][2] = 1
        custom_grid[3][2] = 1

        websocket.send_json({
            "type": "init",
            "width": 10,
            "height": 10,
            "boundary_mode": "bounded",
            "initial_grid": custom_grid
        })
        data = websocket.receive_json()
        assert data["type"] == "state_update"
        assert len(data["grid"]) == 10
        assert len(data["grid"][0]) == 10
        assert data["live_count"] == 3
        assert data["grid"][1][2] == 1


def test_websocket_validation_error():
    with client.websocket_connect("/ws/game") as websocket:
        websocket.receive_json()  # discard initial

        # Invalid speed parameter (exceeds le=30 constraint)
        websocket.send_json({"type": "set_speed", "speed": 100})
        data = websocket.receive_json()
        assert data["type"] == "error"
        assert "Validation Error" in data["message"]


def test_websocket_unknown_command():
    with client.websocket_connect("/ws/game") as websocket:
        websocket.receive_json()  # discard initial

        websocket.send_json({"type": "unknown_cmd"})
        data = websocket.receive_json()
        assert data["type"] == "error"
        assert "Unknown command type" in data["message"]
