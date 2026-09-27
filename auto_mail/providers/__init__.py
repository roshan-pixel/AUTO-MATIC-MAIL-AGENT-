"""Mail client providers (Outlook Web and Gmail Web)."""

from .base_provider import BaseMailProvider
from .outlook import OutlookProvider
from .gmail import GmailProvider

__all__ = [
    "BaseMailProvider",
    "OutlookProvider",
    "GmailProvider",
]
