"""Low-level Chrome DevTools Protocol (CDP) Controller.

Handles trusted synthetic input, virtual keycodes, and DOM file attachments.
Essential for bypassing `isTrusted` protections and triggering Outlook pill validation.
"""

from typing import Dict, Any, List, Optional
import time

class CDPController:
    """Helper to construct and execute standard CDP payloads."""

    @staticmethod
    def enter_key_down() -> Dict[str, Any]:
        """Constructs CDP Input.dispatchKeyEvent for Enter KeyDown."""
        return {
            "method": "Input.dispatchKeyEvent",
            "params": {
                "type": "keyDown",
                "key": "Enter",
                "code": "Enter",
                "windowsVirtualKeyCode": 13,
                "nativeVirtualKeyCode": 13,
                "text": "\r",
                "unmodifiedText": "\r"
            }
        }

    @staticmethod
    def enter_key_up() -> Dict[str, Any]:
        """Constructs CDP Input.dispatchKeyEvent for Enter KeyUp."""
        return {
            "method": "Input.dispatchKeyEvent",
            "params": {
                "type": "keyUp",
                "key": "Enter",
                "code": "Enter",
                "windowsVirtualKeyCode": 13,
                "nativeVirtualKeyCode": 13
            }
        }

    @staticmethod
    def ctrl_enter() -> List[Dict[str, Any]]:
        """Constructs CDP sequence to dispatch Ctrl+Enter (Send shortcut)."""
        return [
            # Control KeyDown
            {
                "method": "Input.dispatchKeyEvent",
                "params": {
                    "type": "keyDown",
                    "key": "Control",
                    "code": "ControlLeft",
                    "windowsVirtualKeyCode": 17,
                    "nativeVirtualKeyCode": 17,
                    "modifiers": 2
                }
            },
            # Enter KeyDown with Ctrl modifier
            {
                "method": "Input.dispatchKeyEvent",
                "params": {
                    "type": "keyDown",
                    "key": "Enter",
                    "code": "Enter",
                    "windowsVirtualKeyCode": 13,
                    "nativeVirtualKeyCode": 13,
                    "modifiers": 2
                }
            },
            # Enter KeyUp
            {
                "method": "Input.dispatchKeyEvent",
                "params": {
                    "type": "keyUp",
                    "key": "Enter",
                    "code": "Enter",
                    "windowsVirtualKeyCode": 13,
                    "nativeVirtualKeyCode": 13,
                    "modifiers": 2
                }
            },
            # Control KeyUp
            {
                "method": "Input.dispatchKeyEvent",
                "params": {
                    "type": "keyUp",
                    "key": "Control",
                    "code": "ControlLeft",
                    "windowsVirtualKeyCode": 17,
                    "nativeVirtualKeyCode": 17
                }
            }
        ]

    @staticmethod
    def set_file_input_files(node_id: int, files: List[str]) -> Dict[str, Any]:
        """CDP DOM.setFileInputFiles for silent multi-file attachment."""
        return {
            "method": "DOM.setFileInputFiles",
            "params": {
                "nodeId": node_id,
                "files": files
            }
        }
