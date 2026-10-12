import asyncio
import base64
import io
import json
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from PIL import Image

STEALTH_JS = """
Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
const originalQuery = window.navigator.mediaDevices.queryDevice;
window.navigator.mediaDevices.queryDevice = function() { return originalQuery.apply(this, arguments); };
"""

@dataclass
class InteractiveElement:
    index: int
    role: str
    name: str
    text: str
    bounding_box: Dict[str, float]
    selector: str

@dataclass
class BrowserState:
    url: str
    title: str
    elements: List[InteractiveElement]
    screenshot_b64: str
    viewport_size: Dict[str, int]

class BrowserEngine:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self._playwright = None

    async def start(self):
        self._playwright = await async_playwright().start()
        self.browser = await self._playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--window-size=1920,1080'
            ]
        )
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        self.page = await self.context.new_page()
        await self.page.add_init_script(STEALTH_JS)
        return self.page

    async def stop(self):
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self._playwright:
            await self._playwright.stop()

    async def navigate(self, url: str):
        if not self.page:
            raise RuntimeError("Browser not started")
        await self.page.goto(url, wait_until='domcontentloaded', timeout=30000)
        await self.page.wait_for_timeout(500)

    async def get_state(self) -> BrowserState:
        if not self.page:
            raise RuntimeError("Browser not started")
        
        url = self.page.url
        title = await self.page.title()
        elements = await self._extract_interactive_elements()
        screenshot_b64 = await self._capture_screenshot()
        viewport = self.page.viewport_size or {'width': 1920, 'height': 1080}
        
        return BrowserState(
            url=url,
            title=title,
            elements=elements,
            screenshot_b64=screenshot_b64,
            viewport_size=viewport
        )

    async def _extract_interactive_elements(self) -> List[InteractiveElement]:
        if not self.page:
            return []
        
        elements = await self.page.evaluate("""() => {
            const selectors = ['button', 'a', 'input', 'textarea', 'select', '[role="button"]', '[role="link"]', '[role="textbox"]', '[onclick]'];
            const all = [];
            let idx = 0;
            for (const sel of selectors) {
                document.querySelectorAll(sel).forEach(el => {
                    const rect = el.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0 && rect.x >= 0 && rect.y >= 0) {
                        all.push({
                            index: idx++,
                            role: el.getAttribute('role') || el.tagName.toLowerCase(),
                            name: el.getAttribute('name') || el.getAttribute('aria-label') || el.textContent?.substring(0, 50) || '',
                            text: el.textContent?.substring(0, 100) || '',
                            bounding_box: {x: rect.x, y: rect.y, width: rect.width, height: rect.height},
                            selector: el.tagName + (el.id ? '#' + el.id : '') + (el.className ? '.' + el.className.split(' ')[0] : '')
                        });
                    }
                });
            }
            return all;
        }""")
        
        return [InteractiveElement(**e) for e in elements[:50]]

    async def _capture_screenshot(self) -> str:
        if not self.page:
            return ""
        img_bytes = await self.page.screenshot(type='jpeg', quality=70)
        return base64.b64encode(img_bytes).decode()

    async def click(self, index: int, elements: List[InteractiveElement]):
        if not self.page or index >= len(elements):
            return False
        el = elements[index]
        try:
            await self.page.click(el.selector, timeout=5000)
            await self.page.wait_for_timeout(300)
            return True
        except Exception:
            return False

    async def type_text(self, text: str):
        if not self.page:
            return False
        await self.page.keyboard.type(text)
        await self.page.wait_for_timeout(200)
        return True

    async def scroll(self, direction: str = 'down'):
        if not self.page:
            return False
        if direction == 'down':
            await self.page.evaluate('window.scrollBy(0, 500)')
        else:
            await self.page.evaluate('window.scrollBy(0, -500)')
        await self.page.wait_for_timeout(300)
        return True

    async def press(self, key: str):
        if not self.page:
            return False
        await self.page.keyboard.press(key)
        await self.page.wait_for_timeout(200)
        return True

    async def download_file(self, path: str) -> Optional[str]:
        if not self.page:
            return None
        try:
            async with self.page.expect_download() as download_info:
                await self.page.click('text*=Download')
            download = await download_info.value
            await download.save_as(path)
            return path
        except Exception:
            return None