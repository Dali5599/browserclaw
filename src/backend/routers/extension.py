from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/extension", tags=["extension"])

class SessionHandoffRequest(BaseModel):
    url: str
    title: Optional[str] = ""
    cookies: List[Dict[str, Any]] = []
    localStorage: Dict[str, str] = {}
    actions: List[Dict[str, Any]] = []

@router.post("/handoff")
async def handoff_session(payload: SessionHandoffRequest):
    try:
        logger.info(f"Received session handoff for URL: {payload.url} with {len(payload.actions)} recorded actions.")
        session_id = f"ext-sess-{abs(hash(payload.url))}"
        return {
            "status": "success",
            "message": "Session successfully handed off to BrowserClaw backend.",
            "sessionId": session_id,
            "actionsRecorded": len(payload.actions)
        }
    except Exception as e:
        logger.error(f"Error handling session handoff: {e}")
        raise HTTPException(status_code=500, detail=str(e))
