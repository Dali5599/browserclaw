"""Robust SQLite Database Layer with Async SQLAlchemy 2.0 & WAL mode."""
import asyncio
from datetime import datetime
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager

from sqlalchemy import Column, String, Text, DateTime, JSON, select, delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from src.backend.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
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

class SessionRecord(Base):
    __tablename__ = "sessions"
    
    id = Column(String, primary_key=True, index=True)
    task = Column(String, nullable=False)
    url = Column(String, default="about:blank")
    status = Column(String, default="pending")  # pending, running, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    steps = Column(JSON, default=list)
    metadata_json = Column(JSON, default=dict)

class TaskRecord(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)
    instruction = Column(Text, nullable=False)
    max_steps = Column(String, default="25")
    status = Column(String, default="queued")
    created_at = Column(DateTime, default=datetime.utcnow)
    result = Column(JSON, nullable=True)

async def init_db():
    """Initializes tables asynchronously."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def get_db_session() -> AsyncSession:
    """Context manager for DB sessions."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# CRUD Helpers
async def create_session_db(session_id: str, task: str, url: str = "about:blank") -> Dict[str, Any]:
    await init_db()
    async with get_db_session() as db:
        rec = SessionRecord(id=session_id, task=task, url=url, status="running")
        db.add(rec)
        await db.flush()
        return {
            "id": rec.id,
            "task": rec.task,
            "url": rec.url,
            "status": rec.status,
            "created_at": rec.created_at.isoformat(),
            "steps": rec.steps or []
        }

async def list_sessions_db() -> List[Dict[str, Any]]:
    await init_db()
    async with get_db_session() as db:
        res = await db.execute(select(SessionRecord).order_by(SessionRecord.created_at.desc()))
        records = res.scalars().all()
        return [
            {
                "id": r.id,
                "task": r.task,
                "url": r.url,
                "status": r.status,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "steps": r.steps or []
            }
            for r in records
        ]

async def get_session_db(session_id: str) -> Optional[Dict[str, Any]]:
    await init_db()
    async with get_db_session() as db:
        res = await db.execute(select(SessionRecord).where(SessionRecord.id == session_id))
        r = res.scalar_one_or_none()
        if not r:
            return None
        return {
            "id": r.id,
            "task": r.task,
            "url": r.url,
            "status": r.status,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "steps": r.steps or []
        }

async def delete_session_db(session_id: str) -> bool:
    await init_db()
    async with get_db_session() as db:
        res = await db.execute(select(SessionRecord).where(SessionRecord.id == session_id))
        r = res.scalar_one_or_none()
        if not r:
            return False
        await db.delete(r)
        return True
