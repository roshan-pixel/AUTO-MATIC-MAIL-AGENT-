"""Abstract Base Provider for Web Mail Clients."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from ..models import EmailMessage, Recipient
from ..drivers.base import BaseMailDriver

class BaseMailProvider(ABC):
    """Abstract base class for Outlook, Gmail, and other webmail providers."""

    def __init__(self, driver: BaseMailDriver):
        self.driver = driver

    @abstractmethod
    def open_mailbox(self) -> bool:
        """Navigates to the mailbox homepage or inbox."""
        pass

    @abstractmethod
    def open_compose(self) -> bool:
        """Triggers the new mail compose dialog/pane."""
        pass

    @abstractmethod
    def set_recipients(self, recipients: List[Recipient]) -> bool:
        """Inputs recipients into To, Cc, and Bcc fields and tokenizes chips."""
        pass

    @abstractmethod
    def set_subject(self, subject: str) -> bool:
        """Sets the email subject."""
        pass

    @abstractmethod
    def set_body(self, html_content: str) -> bool:
        """Sets the email body into the contentEditable rich-text editor."""
        pass

    @abstractmethod
    def add_attachments(self, file_paths: List[str]) -> bool:
        """Uploads file attachments."""
        pass

    @abstractmethod
    def verify_readiness(self) -> Dict[str, Any]:
        """Inspects recipient pills, subject, and body for errors before send."""
        pass

    @abstractmethod
    def send(self) -> bool:
        """Clicks Send or triggers keyboard shortcut."""
        pass

    @abstractmethod
    def verify_sent(self, timeout_sec: float = 10.0) -> bool:
        """Verifies that the message was successfully dispatched."""
        pass
