# Conway's Game of Life — Full-Stack Realtime Web Application

A clean, modular, and performant full-stack implementation of **Conway's Game of Life** built with Next.js 14 (React, TypeScript, HTML Canvas) and FastAPI (Python, WebSockets, Pytest).

---

## Architecture Overview

```text
Browser (Next.js 14 React Frontend)
   │
   ├── HTTP (Fetch static pattern metadata: GET /api/patterns)
   │
   └── WebSocket (Bi-directional realtime stream: /ws/game)
          │
          ▼
FastAPI Server (Python)
   ├── Connection Manager & Event Router
   ├── Background Asyncio Ticker Loop (Dynamic FPS)
   └── Pydantic Schema Validation
          │
          ▼
Simulation Domain Engine (Pure Python)
   ├── Board Model (Matrix Grid & Boundary Handling)
   ├── Rules Evaluator (Parallel Cell Transitions)
   └── Pattern Loader (Coordinate Bounding Box Placement)
```

The core simulation engine is **completely independent** from FastAPI and WebSockets, allowing the Game of Life logic to be fully unit tested without starting a web server.

---

## Key Features

- **Interactive HTML Canvas Board**: High-efficiency 2D Canvas matrix supporting click-to-draw/erase and continuous drag painting.
- **Bi-directional WebSocket Control**: Realtime start, pause, single-step forward, reset, dynamic tick speed (1–30 Hz), and live grid cell toggling.
- **Preset Pattern Selector**: Catalog of pre-configured Life patterns including Still Lifes (*Block*, *Beehive*), Oscillators (*Blinker*, *Toad*, *Beacon*, *Pulsar*), Spaceships (*Glider*), and Guns (*Gosper Glider Gun*).
- **Dual Boundary Modes**:
  - **Toroidal (Wrapping)**: Grid edges wrap around top-to-bottom and left-to-right.
  - **Bounded**: Off-grid neighbors are strictly treated as dead (`0`).
- **Resilient Connection Handling**: Auto-reconnect with exponential fallback, connection status feedback, and server-side ticker task cleanup.

---

## Tech Stack

- **Frontend**: Next.js 14, React 18, TypeScript, HTML5 Canvas 2D API, Vanilla CSS with custom properties.
- **Backend**: Python 3.12, FastAPI, Starlette WebSockets, Pydantic v2, Uvicorn.
- **Testing**: Pytest (33 unit and integration tests), TypeScript `tsc --noEmit`, Next.js production build compiler.

---

## Getting Started

### Prerequisites

- **Python**: 3.10+ (Conda environment recommended)
- **Node.js**: v18+ & `npm`

---

### Backend Setup & Execution

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Activate your Python environment and install dependencies:
   ```bash
   conda activate myenv
   pip install -r requirements.txt
   ```

3. Start the FastAPI development server:
   ```bash
   fastapi dev app/main.py
   ```
   The backend will run at `http://127.0.0.1:8000`.

---

### Frontend Setup & Execution

1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```
   Open `http://localhost:3000` in your web browser.

---

## Running Test Suites

### Backend Tests (Pytest)

Run all 33 unit and integration tests:

```bash
cd backend
python -m pytest tests/ -v
```

**Coverage includes**:
- Conway's 4 rules (underpopulation, survival, overpopulation, reproduction)
- Still lifes, Oscillators, and Glider multi-generation displacement
- Toroidal and Bounded boundary calculations
- FastAPI REST routes (`/api/health`, `/api/patterns`, `/api/board/init`, `/api/board/preset`)
- WebSocket endpoint `/ws/game` message handling and error responses

### Frontend Type Validation & Build

```bash
cd frontend
npx tsc --noEmit
npx next build
```

---

## API & WebSocket Reference

### REST API

- `GET /api/health` — Service health check.
- `GET /api/patterns` — Retrieve metadata list of pre-configured patterns.
- `POST /api/board/init` — Stateless initialization of board state with dimension and grid validation.
- `POST /api/board/preset` — Center pattern preset on grid statelessly.

### WebSocket Protocol (`/ws/game`)

#### Client Messages (`JSON`)
- `{"type": "start"}` — Start continuous simulation loop.
- `{"type": "pause"}` — Pause simulation loop.
- `{"type": "step"}` — Advance simulation by 1 generation.
- `{"type": "reset"}` — Reset board grid cells and generation counter.
- `{"type": "set_speed", "speed": 15}` — Set simulation speed (1–30 Hz).
- `{"type": "set_cell", "x": 10, "y": 12, "alive": true}` — Toggle specific cell state.
- `{"type": "load_preset", "pattern_id": "glider"}` — Center preset on grid and pause.
- `{"type": "init", "width": 50, "height": 50, "boundary_mode": "bounded"}` — Re-initialize grid properties.

#### Server Messages (`JSON`)
- `{"type": "state_update", "generation": 42, "grid": [[...]], "live_count": 128, "is_running": true, "speed": 15, "boundary_mode": "toroidal"}`
- `{"type": "error", "message": "Validation Error: ..."}`

---

## Design Decisions

1. **Decoupled Simulation Engine**: `Board` and `Engine` classes have zero dependencies on web frameworks, allowing rapid pure-Python unit testing.
2. **HTML5 2D Canvas over DOM Grid**: Rendering a 50x50 (2,500 cells) matrix via HTML Canvas achieves 60+ FPS performance without React DOM node thrashing.
3. **Single Async Ticker Loop**: Simulation runs on a background `asyncio` task loop that yields control via `asyncio.sleep()`, preventing duplicate ticker task accumulation.
4. **Optimistic Local State Update**: Interactive canvas cell drawing immediately updates local React state for instantaneous user feedback while transmitting WebSocket state sync.
