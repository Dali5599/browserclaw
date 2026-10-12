from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os

from src.backend.routers.sessions import router as sessions_router
from src.backend.routers.tasks import router as tasks_router
from src.backend.routers.ws import router as ws_router

app = FastAPI(
    title="BrowserClaw API",
    description="Autonomous AI Web Agent with Real-Time Playwright Control & React Dashboard",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "browserclaw",
        "version": "1.0.0",
        "engine": "playwright"
    }

# Include routers
app.include_router(sessions_router)
app.include_router(tasks_router)
app.include_router(ws_router)

# Mount frontend build if available
frontend_dist = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if frontend_dist.is_dir():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
