"""AUTO-MATIC-MAIL-AGENT: Autonomous Email Dispatch & Management Agent for Outlook and Gmail.

Provides multi-driver browser automation (via Kimi WebBridge / Chrome DevTools Protocol / Playwright)
and protocol fallbacks (SMTP/IMAP), equipped with recipient chip validation, contentEditable rich-text
rendering, zero-leak privacy protection, and legal grievance templates.
"""

__version__ = "1.0.0"
__author__ = "Roshan Rathore"

from .models import EmailMessage, Recipient, Attachment, ProviderType
from .agent import MailAgent
from .exceptions import (
    MailAgentError,
    RecipientValidationError,
    DriverConnectionError,
    ComposeTimeoutError,
    DeliveryFailedError,
)

__all__ = [
    "EmailMessage",
    "Recipient",
    "Attachment",
    "ProviderType",
    "MailAgent",
    "MailAgentError",
    "RecipientValidationError",
    "DriverConnectionError",
    "ComposeTimeoutError",
    "DeliveryFailedError",
]
