import pytest
import asyncio
from fastapi.testclient import TestClient
from src.backend.app.main import app
from src.backend.config import settings
from src.backend.services.browser import BrowserState, InteractiveElement, STEALTH_JS
from src.backend.database.db import create_session_db, get_session_db, delete_session_db

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "browserclaw"
    assert data["engine"] == "playwright"

def test_session_lifecycle():
    payload = {"task": "Verify hacker news headline", "url": "https://news.ycombinator.com"}
    create_res = client.post("/api/sessions", json=payload)
    assert create_res.status_code == 200
    session = create_res.json()
    assert "id" in session
    sess_id = session["id"]

    list_res = client.get("/api/sessions")
    assert list_res.status_code == 200
    sessions = list_res.json()
    assert any(s["id"] == sess_id for s in sessions)

    get_res = client.get(f"/api/sessions/{sess_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == sess_id

    del_res = client.delete(f"/api/sessions/{sess_id}")
    assert del_res.status_code == 200

    get_res_404 = client.get(f"/api/sessions/{sess_id}")
    assert get_res_404.status_code == 404

def test_task_dispatch():
    payload = {"instruction": "Scrape trending repos", "max_steps": 10}
    res = client.post("/api/tasks", json=payload)
    assert res.status_code == 200
    task = res.json()
    assert "id" in task
    assert task["instruction"] == "Scrape trending repos"

    task_id = task["id"]
    get_res = client.get(f"/api/tasks/{task_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == task_id

def test_browser_models():
    elem = InteractiveElement(
        index=1,
        role="button",
        name="Submit",
        text="Click Me",
        bounding_box={"x": 10.0, "y": 20.0, "width": 100.0, "height": 30.0},
        selector="#submit-btn"
    )
    assert elem.role == "button"
    assert elem.selector == "#submit-btn"

    state = BrowserState(
        url="https://example.com",
        title="Example Domain",
        elements=[elem],
        screenshot_b64="data:image/png;base64,mock",
        viewport_size={"width": 1280, "height": 800}
    )
    assert state.title == "Example Domain"
    assert len(state.elements) == 1
    assert state.viewport_size["width"] == 1280

def test_stealth_injection_content():
    assert "webdriver" in STEALTH_JS
    assert "navigator" in STEALTH_JS

def test_database_crud_direct():
    async def _test():
        test_id = "test_crud_123"
        created = await create_session_db(test_id, "Test task execution", "https://example.com")
        assert created["id"] == test_id
        assert created["status"] == "running"

        fetched = await get_session_db(test_id)
        assert fetched is not None
        assert fetched["task"] == "Test task execution"

        deleted = await delete_session_db(test_id)
        assert deleted is True

        notFound = await get_session_db(test_id)
        assert notFound is None
    asyncio.run(_test())

def test_config_defaults():
    assert settings.PORT == 8000
    assert settings.HEADLESS is True
    assert "sqlite+aiosqlite" in settings.DATABASE_URL
