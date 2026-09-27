"""Custom exceptions for the Mail Agent framework."""

class MailAgentError(Exception):
    """Base exception for all auto-mail agent errors."""
    pass

class DriverConnectionError(MailAgentError):
    """Raised when connecting to automation daemon (WebBridge/CDP) fails."""
    pass

class RecipientValidationError(MailAgentError):
    """Raised when an email recipient fails syntax or platform pill/chip validation."""
    def __init__(self, email: str, reason: str):
        super().__init__(f"Recipient validation failed for '{email}': {reason}")
        self.email = email
        self.reason = reason

class ComposeTimeoutError(MailAgentError):
    """Raised when the mail client compose dialog or elements do not appear within timeout."""
    pass

class ElementInteractionError(MailAgentError):
    """Raised when clicking, typing, or dispatching events to a DOM node fails."""
    pass

class DeliveryFailedError(MailAgentError):
    """Raised when email submission fails or returns an unrecoverable bounce/error."""
    pass

class DataSanitizationError(MailAgentError):
    """Raised when sensitive data (e.g. credit card PAN or CVV) is detected in payload."""
    pass
