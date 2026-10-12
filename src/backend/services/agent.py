import logging
import os
from typing import Dict, Any
from src.backend.services.browser import browser_service
from src.backend.services.vision import vision_service

logger = logging.getLogger("browserclaw.agent")

class AgentService:
    def __init__(self):
        pass

    async def execute_task(self, session_id: str, goal: str) -> Dict[str, Any]:
        logger.info(f"Executing task for session {session_id} with goal: {goal}")
        
        # Ensure browser page exists
        page = await browser_service.get_or_create_page(session_id)
        
        # Take screenshot for vision processing
        screenshot_dir = "/tmp/browserclaw"
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, f"{session_id}.png")
        
        await page.screenshot(path=screenshot_path)
        
        # Run Vision-LLM bounding box detection based on goal
        detections = vision_service.detect_bounding_box(screenshot_path, goal)
        logger.info(f"Detections found: {detections}")
        
        action_taken = "none"
        if detections:
            box = detections[0]["box_2d"]
            # Convert normalized 1000 coordinates to viewport pixels
            viewport = page.viewport_size or {"width": 1280, "height": 720}
            x = (box[1] / 1000.0) * viewport["width"]
            y = (box[0] / 1000.0) * viewport["height"]
            
            logger.info(f"Clicking at calculated coordinates: x={x}, y={y}")
            await page.mouse.click(x, y)
            action_taken = f"clicked at ({x}, {y}) based on vision detection"
        else:
            logger.warning("No bounding box detected by Vision-LLM, performing fallback or doing nothing.")
            action_taken = "no bounding box detected"

        return {
            "status": "completed",
            "goal": goal,
            "detections": detections,
            "action_taken": action_taken
        }

agent_service = AgentService()
