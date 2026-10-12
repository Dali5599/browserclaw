import pytest
from src.backend.services.browser import BrowserState, InteractiveElement, STEALTH_JS, BrowserService

def test_browser_imports():
    assert BrowserState is not None
    assert InteractiveElement is not None
    assert STEALTH_JS is not None

@pytest.mark.asyncio
async def test_browser_service():
    service = BrowserService()
    await service.start()
    assert service.is_running is True
    state = await service.navigate("https://example.com")
    assert state.url == "https://example.com"
    await service.stop()
    assert service.is_running is False
