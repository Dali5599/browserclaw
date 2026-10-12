from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.backend.routers import tasks, ws, sessions
from src.backend.routers import extension
from src.backend.database.db import init_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="BrowserClaw API",
    description="Backend API for BrowserClaw autonomous browser agent & extension handoff",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router)
app.include_router(ws.router)
app.include_router(sessions.router)
app.include_router(extension.router)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting BrowserClaw backend...")
    init_db()

@app.get("/")
async def root():
    return {"status": "ok", "service": "BrowserClaw API"}
