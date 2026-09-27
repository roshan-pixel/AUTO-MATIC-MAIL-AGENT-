"""Automation and protocol drivers for mail clients."""

from .base import BaseMailDriver
from .cdp_controller import CDPController
from .webbridge import WebBridgeDriver
from .playwright_driver import PlaywrightDriver
from .smtp_driver import SMTPDriver

__all__ = [
    "BaseMailDriver",
    "CDPController",
    "WebBridgeDriver",
    "PlaywrightDriver",
    "SMTPDriver",
]
