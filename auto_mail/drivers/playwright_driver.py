"""Playwright Driver implementation for standalone browser execution."""

from typing import Dict, Any, List, Optional
from pathlib import Path
import time

from .base import BaseMailDriver
from ..exceptions import DriverConnectionError, ElementInteractionError

class PlaywrightDriver(BaseMailDriver):
    """Direct Playwright automation driver (standalone / CI environments)."""

    def __init__(self, page: Any = None, headless: bool = False, user_data_dir: Optional[str] = None):
        self.page = page
        self.headless = headless
        self.user_data_dir = user_data_dir
        self._browser = None
        self._context = None
        self._playwright = None

    def start(self):
        """Initializes playwright browser context if not passed."""
        if self.page:
            return
        try:
            from playwright.sync_api import sync_playwright
            self._playwright = sync_playwright().start()
            if self.user_data_dir:
                self._context = self._playwright.chromium.launch_persistent_context(
                    self.user_data_dir,
                    headless=self.headless,
                    args=["--disable-blink-features=AutomationControlled"]
                )
                self.page = self._context.pages[0] if self._context.pages else self._context.new_page()
            else:
                self._browser = self._playwright.chromium.launch(headless=self.headless)
                self._context = self._browser.new_context()
                self.page = self._context.new_page()
        except ImportError:
            raise DriverConnectionError("Playwright is not installed. Run 'pip install playwright && playwright install'.")

    def stop(self):
        """Closes browser context and playwright session."""
        if self._context:
            self._context.close()
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()

    def navigate(self, url: str) -> bool:
        self.start()
        self.page.goto(url, wait_until="domcontentloaded")
        return True

    def evaluate(self, js_code: str) -> Any:
        self.start()
        return self.page.evaluate(js_code)

    def click(self, selector: str) -> bool:
        self.start()
        self.page.click(selector)
        return True

    def type_text(self, selector: str, text: str) -> bool:
        self.start()
        el = self.page.locator(selector).first
        el.click()
        el.type(text)
        return True

    def dispatch_enter(self) -> bool:
        self.start()
        self.page.keyboard.press("Enter")
        time.sleep(0.1)
        return True

    def dispatch_key_combination(self, key: str, modifiers: List[str]) -> bool:
        self.start()
        mod_prefix = "+".join(modifiers)
        combo = f"{mod_prefix}+{key}" if mod_prefix else key
        self.page.keyboard.press(combo)
        return True

    def take_screenshot(self, output_path: Path) -> Path:
        self.start()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.page.screenshot(path=str(output_path), full_page=True)
        return output_path

    def upload_file(self, selector: str, file_path: Path) -> bool:
        self.start()
        self.page.set_input_files(selector, str(file_path))
        return True
