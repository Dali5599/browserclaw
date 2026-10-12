import os
from pathlib import Path
from typing import List

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings:
    """Production configuration for BrowserClaw."""
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Playwright Automation Engine
    HEADLESS: bool = os.getenv("HEADLESS", "true").lower() == "true"
    STEALTH_MODE: bool = os.getenv("STEALTH_MODE", "true").lower() == "true"
    DEFAULT_VIEWPORT_WIDTH: int = int(os.getenv("VIEWPORT_WIDTH", "1280"))
    DEFAULT_VIEWPORT_HEIGHT: int = int(os.getenv("VIEWPORT_HEIGHT", "800"))
    USER_AGENT: str = os.getenv(
        "USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    
    # SQLite Database with WAL mode
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", str(BASE_DIR / "browserclaw.db"))
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite+aiosqlite:///{DATABASE_PATH}")
    
    # WebSocket & Telemetry
    WS_HEARTBEAT_INTERVAL: int = int(os.getenv("WS_HEARTBEAT_INTERVAL", "15000"))
    
    # Security & CORS
    CORS_ORIGINS: List[str] = ["*"]
    SECRET_KEY: str = os.getenv("SECRET_KEY", "browserclaw-super-secret-key-2026")

settings = Settings()
