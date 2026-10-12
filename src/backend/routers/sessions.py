import uuid
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from src.backend.database.db import (
    create_session_db,
    list_sessions_db,
    get_session_db,
    delete_session_db
)

router = APIRouter(prefix="/api/sessions", tags=["sessions"])

@router.get("")
async def list_sessions():
    """Retrieve all active and archived automation sessions."""
    return await list_sessions_db()

@router.post("")
async def create_session(data: Dict[str, Any]):
    """Launch a new browser automation session with task tracking."""
    session_id = f"sess_{uuid.uuid4().hex[:8]}"
    task = data.get("task", "Autonomous web exploration")
    url = data.get("url", "https://news.ycombinator.com")
    session = await create_session_db(session_id, task, url)
    return session

@router.get("/{session_id}")
async def get_session(session_id: str):
    """Fetch live details, thought timeline, and action history for a session."""
    session = await get_session_db(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.delete("/{session_id}")
async def delete_session(session_id: str):
    """Terminate and purge an automation session."""
    success = await delete_session_db(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "deleted", "id": session_id}
