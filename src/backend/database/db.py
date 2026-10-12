"""Database layer for browserclaw with SQLite (WAL mode)."""
import sqlite3
import asyncio
from contextlib import asynccontextmanager
from typing import Optional, List, Dict, Any

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB as PGJSON
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base, relationship

from .config import settings

# SQLAlchemy engine with WAL mode
engine = create_async_engine(
    settings.DATABASE_PATH,
    connect_args={"check_same_thread": False},
    echo=False,
    pool_pre_ping=True,
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


class Session(Base):
    """SQLAlchemy model for sessions."""
    __tablename__ = "sessions"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    task = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, running, paused, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    last_activity = Column(DateTime, nullable=True)
    user_id = Column(String, nullable=True)
    config = Column(JSON, nullable=True)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "task": self.task,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
            "user_id": self.user_id,
            "config": self.config,
        }


class ActionStep(Base):
    """SQLAlchemy model for action steps."""
    __tablename__ = "action_steps"
    
    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), index=True, nullable=False)
    step_number = Column(Integer, nullable=False)
    action_type = Column(String, nullable=False)  # click, type, scroll, wait, navigate, screenshot
    target = Column(String, nullable=True)
    element_id = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    status = Column(String, default="pending")  # pending, executed, failed
    result = Column(Text, nullable=True)
    duration_ms = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    screenshot = Column(String, nullable=True)  # base64 encoded image
    error = Column(Text, nullable=True)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "session_id": self.session_id,
            "step_number": self.step_number,
            "action_type": self.action_type,
            "target": self.target,
            "element_id": self.element_id,
            "description": self.description,
            "status": self.status,
            "result": self.result,
            "duration_ms": self.duration_ms,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "screenshot": self.screenshot,
            "error": self.error,
        }


class Artifact(Base):
    """SQLAlchemy model for artifacts (screenshots, documents)."""
    __tablename__ = "artifacts"
    
    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), index=True, nullable=False)
    artifact_type = Column(String, nullable=False)  # screenshot, document, video
    name = Column(String, nullable=False)
    data = Column(Text, nullable=True)  # base64 for images
    file_path = Column(String, nullable=True)
    mime_type = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "session_id": self.session_id,
            "artifact_type": self.artifact_type,
            "name": self.name,
            "data": self.data,
            "file_path": self.file_path,
            "mime_type": self.mime_type,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class BrowserState(Base):
    """SQLAlchemy model for browser state snapshots."""
    __tablename__ = "browser_states"
    
    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), index=True, nullable=False)
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    viewport = Column(dict)  # x, y, width, height
    screenshot = Column(String, nullable=True)
    dom_snapshot = Column(PGJSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "session_id": self.session_id,
            "url": self.url,
            "title": self.title,
            "viewport": self.viewport,
            "screenshot": self.screenshot,
            "dom_snapshot": self.dom_snapshot,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


def init_db():
    """Initialize the database tables."""
    async def create_tables():
        await engine.begin().execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                task TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                last_activity TIMESTAMP,
                user_id TEXT,
                config JSON
            )
        """)
        
        await engine.begin().execute("""
            CREATE TABLE IF NOT EXISTS action_steps (
                id TEXT PRIMARY KEY,
                session_id TEXT REFERENCES sessions(id) ON DELETE CASCADE,
                step_number INTEGER NOT NULL,
                action_type TEXT NOT NULL,
                target TEXT,
                element_id TEXT,
                description TEXT,
                status TEXT DEFAULT 'pending',
                result TEXT,
                duration_ms REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                screenshot TEXT,
                error TEXT
            )
        """)
        
        await engine.begin().execute("""
            CREATE TABLE IF NOT EXISTS artifacts (
                id TEXT PRIMARY KEY,
                session_id TEXT REFERENCES sessions(id) ON DELETE CASCADE,
                artifact_type TEXT NOT NULL,
                name TEXT NOT NULL,
                data TEXT,
                file_path TEXT,
                mime_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await engine.begin().execute("""
            CREATE TABLE IF NOT EXISTS browser_states (
                id TEXT PRIMARY KEY,
                session_id TEXT REFERENCES sessions(id) ON DELETE CASCADE,
                url TEXT NOT NULL,
                title TEXT NOT NULL,
                viewport JSON,
                screenshot TEXT,
                dom_snapshot JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    
    asyncio.run(create_tables())


@asynccontextmanager
async def get_db_session() -> AsyncSession:
    """Async context manager for database sessions."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Export for convenience
session_model = Session
action_step_model = ActionStep
artifact_model = Artifact
browser_state_model = BrowserState
init_db = init_db
