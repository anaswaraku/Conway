from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.api.websocket import router as ws_router

app = FastAPI(
    title="Conway's Game of Life API",
    description="Backend API and WebSocket engine for Conway's Game of Life",
    version="1.0.0"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount REST API Router
app.include_router(api_router)

# Mount WebSocket Router
app.include_router(ws_router)

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "game-of-life-backend"}
