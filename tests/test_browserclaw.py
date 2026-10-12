import pytest
from fastapi.testclient import TestClient
from src.backend.app.main import app
from src.backend.config import Settings
from src.backend.services.browser import BrowserState, InteractiveElement

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "browserclaw"
    assert data["engine"] == "playwright"

def test_session_lifecycle():
    # 1. Create
    payload = {"task": "Verify hacker news headline", "url": "https://news.ycombinator.com"}
    create_res = client.post("/api/sessions", json=payload)
    assert create_res.status_code == 200
    session = create_res.json()
    assert "id" in session
    sess_id = session["id"]

    # 2. List
    list_res = client.get("/api/sessions")
    assert list_res.status_code == 200
    sessions = list_res.json()
    assert any(s["id"] == sess_id for s in sessions)

    # 3. Get
    get_res = client.get(f"/api/sessions/{sess_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == sess_id

    # 4. Delete
    del_res = client.delete(f"/api/sessions/{sess_id}")
    assert del_res.status_code == 200

    # 5. Get Not Found
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
