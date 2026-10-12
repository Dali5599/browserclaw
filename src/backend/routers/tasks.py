from fastapi import APIRouter, HTTPException
from typing import Dict, Any

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

tasks_store: Dict[str, Dict[str, Any]] = {}

@router.get("")
async def list_tasks():
    return list(tasks_store.values())

@router.post("")
async def dispatch_task(data: Dict[str, Any]):
    task_id = f"task_{len(tasks_store) + 1}"
    task = {
        "id": task_id,
        "instruction": data.get("instruction", ""),
        "max_steps": data.get("max_steps", 25),
        "status": "queued"
    }
    tasks_store[task_id] = task
    return task

@router.get("/{task_id}")
async def get_task(task_id: str):
    if task_id not in tasks_store:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks_store[task_id]
