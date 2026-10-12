import os
from typing import Optional

class Settings:
    """Application configuration from environment variables."""
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Playwright settings
    HEADLESS: bool = os.getenv("HEADLESS", "true").lower() == "true"
    STEALTH_MODE: bool = os.getenv("STEALTH_MODE", "true").lower() == "true"
    
    # WebSocket settings
    WS_HEARTBEAT_INTERVAL: int = int(os.getenv("WS_HEARTBEAT_INTERVAL", "30000"))
    WS_MAX_MESSAGES: int = int(os.getenv("WS_MAX_MESSAGES", "1000"))
    
    # Database settings
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "/home/nexus/.openclaw/workspace/browserclaw/src/backend/database/browserclaw.db")
    
    # CORS settings
    CORS_ORIGINS: list[str] = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "browserclaw-secret-change-in-production")
    SESSION_TIMEOUT: int = int(os.getenv("SESSION_TIMEOUT", "3600"))  # seconds

settings = Settings()