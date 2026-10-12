from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
import asyncio

router = APIRouter(tags=["websocket"])

@router.websocket("/ws/live")
async def websocket_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data) if data.startswith("{") else {"raw": data}
            response = {
                "event": "agent_frame",
                "timestamp": "2026-10-12T10:00:00Z",
                "viewport": {"width": 1280, "height": 800},
                "status": "active",
                "echo": payload
            }
            await websocket.send_text(json.dumps(response))
    except WebSocketDisconnect:
        pass
