from fastapi import status
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_api_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "ok"


def test_list_preset_patterns():
    response = client.get("/api/patterns")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Ensure glider is present
    ids = [p["id"] for p in data]
    assert "glider" in ids


def test_initialize_default_board():
    response = client.post(
        "/api/board/init",
        json={"width": 40, "height": 30, "boundary_mode": "toroidal"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["width"] == 40
    assert data["height"] == 30
    assert data["boundary_mode"] == "toroidal"
    assert len(data["grid"]) == 30
    assert len(data["grid"][0]) == 40
    assert data["live_count"] == 0


def test_initialize_board_with_custom_grid():
    custom_grid = [
        [0, 1, 0],
        [0, 0, 1],
        [1, 1, 1]
    ]
    response = client.post(
        "/api/board/init",
        json={
            "width": 3,
            "height": 3,
            "boundary_mode": "bounded",
            "initial_grid": custom_grid
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["grid"] == custom_grid
    assert data["live_count"] == 5


def test_initialize_board_mismatched_grid_dimensions():
    # height of grid is 2, but config height is 3
    response = client.post(
        "/api/board/init",
        json={
            "width": 3,
            "height": 3,
            "initial_grid": [[0, 0, 0], [0, 0, 0]]
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_initialize_board_invalid_cell_state():
    # Cell has value 2 (must be 0 or 1)
    response = client.post(
        "/api/board/init",
        json={
            "width": 3,
            "height": 3,
            "initial_grid": [[0, 0, 0], [0, 2, 0], [0, 0, 0]]
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_initialize_board_out_of_bounds_dimensions():
    response = client.post(
        "/api/board/init",
        json={"width": 1, "height": 50}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_initialize_board_invalid_boundary_mode():
    response = client.post(
        "/api/board/init",
        json={"width": 50, "height": 50, "boundary_mode": "invalid_mode"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_load_preset_success():
    response = client.post(
        "/api/board/preset",
        json={"width": 20, "height": 20, "pattern_id": "glider"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["live_count"] == 5


def test_load_non_existent_preset():
    response = client.post(
        "/api/board/preset",
        json={"width": 20, "height": 20, "pattern_id": "non_existent_pattern"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
