from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
from src.backend.services.browser import manager

router = APIRouter(tags=["websocket"])

@router.websocket("/ws/tabs/{tab_id}")
async def websocket_tab_endpoint(websocket: WebSocket, tab_id: str):
    await websocket.accept()
    tab = manager.get_tab(tab_id)
    if not tab:
        await websocket.send_json({"error": "Tab not found or inactive"})
        await websocket.close()
        return

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            action = message.get("action")

            if action == "navigate":
                url = message.get("url")
                if url:
                    await tab.navigate(url)
                    await websocket.send_json({"status": "navigated", "url": url})
                else:
                    await websocket.send_json({"error": "Missing url"})
            elif action == "evaluate":
                script = message.get("script")
                if script:
                    res = await tab.evaluate(script)
                    await websocket.send_json({"status": "evaluated", "result": res})
                else:
                    await websocket.send_json({"error": "Missing script"})
            else:
                await websocket.send_json({"error": f"Unknown action: {action}"})

    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({"error": str(e)})
        await websocket.close()
