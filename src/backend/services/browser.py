from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

STEALTH_JS = """
// Stealth injections to evade bot detection
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
});
window.navigator.chrome = {
    runtime: {},
};
"""

@dataclass
class InteractiveElement:
    id: str
    tag_name: str
    text: str
    x: float
    y: float
    attributes: Dict[str, str] = field(default_factory=dict)
    is_visible: bool = True
    is_enabled: bool = True

@dataclass
class BrowserState:
    url: str
    title: str
    html: str
    screenshot: Optional[str] = None
    elements: List[InteractiveElement] = field(default_factory=list)
    console_logs: List[str] = field(default_factory=list)
    cookies: List[Dict[str, Any]] = field(default_factory=list)

class BrowserService:
    def __init__(self):
        self.current_url: str = ""
        self.is_running: bool = False

    async def start(self) -> None:
        self.is_running = True

    async def stop(self) -> None:
        self.is_running = False

    async def navigate(self, url: str) -> BrowserState:
        self.current_url = url
        return BrowserState(url=url, title="Mocked Page", html="<html></html>")

    async def get_state(self) -> BrowserState:
        return BrowserState(url=self.current_url, title="Mocked Page", html="<html></html>")
