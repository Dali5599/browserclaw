from fastapi import APIRouter, HTTPException
import uuid
from src.backend.models.session import SessionCreate, TabCreate, SessionResponse, TabResponse
from src.backend.services.browser import manager

router = APIRouter(prefix="/sessions", tags=["sessions"])

sessions_store = {} 

@router.post("/", response_model=SessionResponse)
async def create_session(payload: SessionCreate):
    session_id = str(uuid.uuid4())
    await manager.create_context(session_id)
    sessions_store[session_id] = {"status": "active", "tabs": {}}
    return SessionResponse(session_id=session_id, status="active", tabs={})

@router.post("/{session_id}/tabs", response_model=TabResponse)
async def create_tab(session_id: str, payload: TabCreate):
    if session_id not in sessions_store:
        raise HTTPException(status_code=404, detail="Session not found")
    
    tab_id = str(uuid.uuid4())
    tab_session = await manager.create_tab(session_id, tab_id, payload.url)
    sessions_store[session_id]["tabs"][tab_id] = {"url": payload.url, "status": "open"}
    
    return TabResponse(tab_id=tab_id, session_id=session_id, url=payload.url, status="open")

@router.delete("/{session_id}/tabs/{tab_id}")
async def close_tab(session_id: str, tab_id: str):
    if session_id not in sessions_store or tab_id not in sessions_store[session_id]["tabs"]:
        raise HTTPException(status_code=404, detail="Session or Tab not found")
    
    await manager.close_tab(tab_id)
    del sessions_store[session_id]["tabs"][tab_id]
    return {"status": "closed", "tab_id": tab_id}

@router.delete("/{session_id}")
async def close_session(session_id: str):
    if session_id not in sessions_store:
        raise HTTPException(status_code=404, detail="Session not found")
    
    await manager.close_session(session_id)
    del sessions_store[session_id]
    return {"status": "closed", "session_id": session_id}
