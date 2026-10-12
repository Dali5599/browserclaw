from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

router = APIRouter(prefix="/api/sessions", tags=["sessions"])

# In-memory store fallback / reference
sessions_store: Dict[str, Dict[str, Any]] = {}

@router.get("")
async def list_sessions():
    return list(sessions_store.values())

@router.post("")
async def create_session(data: Dict[str, Any]):
    sess_id = f"sess_{len(sessions_store) + 1}"
    session = {
        "id": sess_id,
        "task": data.get("task", "Automated browser workflow"),
        "status": "running",
        "url": data.get("url", "https://news.ycombinator.com"),
        "steps": [],
        "created_at": "2026-10-12T10:00:00Z"
    }
    sessions_store[sess_id] = session
    return session

@router.get("/{session_id}")
async def get_session(session_id: str):
    if session_id not in sessions_store:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions_store[session_id]

@router.delete("/{session_id}")
async def delete_session(session_id: str):
    if session_id not in sessions_store:
        raise HTTPException(status_code=404, detail="Session not found")
    del sessions_store[session_id]
    return {"status": "deleted", "id": session_id}
