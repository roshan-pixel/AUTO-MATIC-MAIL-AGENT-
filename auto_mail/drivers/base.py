"""Base driver interface for mail automation."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from pathlib import Path

class BaseMailDriver(ABC):
    """Abstract base class for all browser and protocol drivers."""

    @abstractmethod
    def navigate(self, url: str) -> bool:
        """Navigates to the specified URL."""
        pass

    @abstractmethod
    def evaluate(self, js_code: str) -> Any:
        """Executes JavaScript within the active web page."""
        pass

    @abstractmethod
    def click(self, selector: str) -> bool:
        """Clicks an element identified by CSS selector or element ref."""
        pass

    @abstractmethod
    def type_text(self, selector: str, text: str) -> bool:
        """Types text into an element."""
        pass

    @abstractmethod
    def dispatch_enter(self) -> bool:
        """Dispatches an Enter key event (CDP or synthetic)."""
        pass

    @abstractmethod
    def dispatch_key_combination(self, key: str, modifiers: List[str]) -> bool:
        """Dispatches a key combination (e.g., Ctrl+Enter)."""
        pass

    @abstractmethod
    def take_screenshot(self, output_path: Path) -> Path:
        """Captures a screenshot of the current page state."""
        pass

    @abstractmethod
    def upload_file(self, selector: str, file_path: Path) -> bool:
        """Attaches a file to a file input element."""
        pass
