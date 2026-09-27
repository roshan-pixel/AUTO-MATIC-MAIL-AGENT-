"""Kimi WebBridge Driver implementation.

Communicates with the user's active browser session via the WebBridge local daemon
at http://127.0.0.1:10086. Leverages real cookies, authenticated accounts, and CDP.
"""

import json
import time
import requests
from typing import Dict, Any, List, Optional
from pathlib import Path

from .base import BaseMailDriver
from .cdp_controller import CDPController
from ..exceptions import DriverConnectionError, ElementInteractionError

class WebBridgeDriver(BaseMailDriver):
    """Driver connecting to real Chrome/Edge browser via Kimi WebBridge daemon."""

    def __init__(
        self,
        daemon_url: str = "http://127.0.0.1:10086",
        session: str = "mail-agent-session",
        timeout: float = 30.0
    ):
        self.daemon_url = daemon_url.rstrip("/")
        self.session = session
        self.timeout = timeout
        self.cdp = CDPController()

    def check_connection(self) -> Dict[str, Any]:
        """Verifies WebBridge daemon and browser extension status."""
        try:
            r = requests.get(f"{self.daemon_url}/status", timeout=self.timeout)
            r.raise_for_status()
            data = r.json()
            if not data.get("running"):
                raise DriverConnectionError("WebBridge daemon is not running.")
            if not data.get("extension_connected"):
                raise DriverConnectionError("Browser extension is not connected to WebBridge daemon.")
            return data
        except requests.RequestException as e:
            raise DriverConnectionError(f"Failed to connect to WebBridge daemon at {self.daemon_url}: {e}")

    def execute_command(self, action: str, args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Dispatches an action to WebBridge /command endpoint."""
        payload = {
            "action": action,
            "session": self.session,
            "args": args or {}
        }
        try:
            r = requests.post(
                f"{self.daemon_url}/command",
                json=payload,
                timeout=self.timeout
            )
            r.raise_for_status()
            res = r.json()
            if not res.get("ok"):
                err = res.get("error", {})
                raise ElementInteractionError(f"WebBridge action '{action}' failed: {err.get('message', res)}")
            return res.get("data", {})
        except requests.RequestException as e:
            raise DriverConnectionError(f"HTTP error communicating with WebBridge: {e}")

    def cdp_call(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Sends raw CDP method and parameters via WebBridge."""
        return self.execute_command("cdp", {"method": method, "params": params})

    def navigate(self, url: str) -> bool:
        """Navigates to URL, attempting to find or borrow an existing tab first."""
        # Try finding existing tab with this host
        try:
            res_find = self.execute_command("find_tab", {"url": url})
            if res_find.get("success"):
                return True
        except Exception:
            pass

        # Otherwise navigate
        res = self.execute_command("navigate", {"url": url, "newTab": False})
        return res.get("success", False)

    def evaluate(self, js_code: str) -> Any:
        """Executes JS in page context and returns result value."""
        res = self.execute_command("evaluate", {"code": js_code})
        return res.get("value")

    def click(self, selector: str) -> bool:
        """Clicks element by CSS selector or WebBridge @e ref."""
        res = self.execute_command("click", {"selector": selector})
        return res.get("success", False)

    def type_text(self, selector: str, text: str) -> bool:
        """Focuses element and inserts text."""
        # Use contentEditable / input friendly injection
        code = f"""(() => {{
            const el = document.querySelector({json.dumps(selector)});
            if (!el) return false;
            el.focus();
            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {{
                el.value = {json.dumps(text)};
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                el.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }} else {{
                document.execCommand('insertText', false, {json.dumps(text)});
            }}
            return true;
        }})()"""
        val = self.evaluate(code)
        return bool(val)

    def dispatch_enter(self) -> bool:
        """Sends native Enter key via CDP to tokenize pills/chips."""
        down = self.cdp.enter_key_down()
        up = self.cdp.enter_key_up()
        self.cdp_call(down["method"], down["params"])
        time.sleep(0.05)
        self.cdp_call(up["method"], up["params"])
        time.sleep(0.1)
        return True

    def dispatch_key_combination(self, key: str, modifiers: List[str]) -> bool:
        """Sends key combinations such as Ctrl+Enter."""
        if key.lower() == "enter" and "ctrl" in [m.lower() for m in modifiers]:
            seq = self.cdp.ctrl_enter()
            for step in seq:
                self.cdp_call(step["method"], step["params"])
                time.sleep(0.03)
            return True
        return False

    def take_screenshot(self, output_path: Path) -> Path:
        """Captures page screenshot to disk."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        res = self.execute_command("screenshot", {
            "format": "png",
            "path": str(output_path)
        })
        return Path(res.get("path", str(output_path)))

    def upload_file(self, selector: str, file_path: Path) -> bool:
        """Uploads file attachment."""
        res = self.execute_command("upload", {
            "selector": selector,
            "files": [str(file_path)]
        })
        return res.get("success", False)
