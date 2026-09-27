"""Standard SMTP Protocol Driver fallback."""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import Dict, Any, List, Optional

from .base import BaseMailDriver
from ..models import EmailMessage
from ..exceptions import DeliveryFailedError

class SMTPDriver(BaseMailDriver):
    """Direct SMTP email dispatch driver."""

    def __init__(
        self,
        smtp_host: str,
        smtp_port: int = 587,
        username: Optional[str] = None,
        password: Optional[str] = None,
        use_tls: bool = True
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls

    def send_message(self, message: EmailMessage) -> bool:
        """Sends EmailMessage via SMTP."""
        msg = MIMEMultipart("alternative")
        msg["Subject"] = message.subject
        msg["From"] = message.sender or self.username or "noreply@auto-mail.local"
        msg["To"] = ", ".join([r.email for r in message.to_recipients])
        if message.cc_recipients:
            msg["Cc"] = ", ".join([r.email for r in message.cc_recipients])

        # Attach text and HTML parts
        if message.body_text:
            msg.attach(MIMEText(message.body_text, "plain", "utf-8"))
        msg.attach(MIMEText(message.body_html, "html", "utf-8"))

        # Attach files
        for att in message.attachments:
            part = MIMEBase("application", "octet-stream")
            with open(att.path, "rb") as f:
                part.set_payload(f.read())
            encoders.encode_base64(part)
            filename = att.filename or att.path.name
            part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
            msg.attach(part)

        all_recipients = [r.email for r in message.recipients]

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                if self.username and self.password:
                    server.login(self.username, self.password)
                server.sendmail(msg["From"], all_recipients, msg.as_string())
            return True
        except Exception as e:
            raise DeliveryFailedError(f"SMTP delivery failed: {e}")

    # Satisfy BaseMailDriver abstract methods (for unified interface)
    def navigate(self, url: str) -> bool: return True
    def evaluate(self, js_code: str) -> Any: return None
    def click(self, selector: str) -> bool: return True
    def type_text(self, selector: str, text: str) -> bool: return True
    def dispatch_enter(self) -> bool: return True
    def dispatch_key_combination(self, key: str, modifiers: List[str]) -> bool: return True
    def take_screenshot(self, output_path: Path) -> Path: return output_path
    def upload_file(self, selector: str, file_path: Path) -> bool: return True
