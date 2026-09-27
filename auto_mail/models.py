"""Data models and abstractions for Mail Agent."""

from enum import Enum
from typing import List, Optional, Dict, Any
from pathlib import Path
import re
from pydantic import BaseModel, Field, field_validator

class ProviderType(str, Enum):
    OUTLOOK = "outlook"
    GMAIL = "gmail"
    SMTP = "smtp"

class RecipientRole(str, Enum):
    TO = "to"
    CC = "cc"
    BCC = "bcc"

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

class Recipient(BaseModel):
    """Represents a validated email recipient."""
    email: str
    name: Optional[str] = None
    role: RecipientRole = RecipientRole.TO
    verified: bool = False

    @field_validator("email")
    def validate_email_syntax(cls, v: str) -> str:
        clean = v.strip().lower()
        if not EMAIL_REGEX.match(clean):
            raise ValueError(f"Invalid email address format: '{v}'")
        return clean

class Attachment(BaseModel):
    """Represents a file attachment."""
    path: Path
    filename: Optional[str] = None
    mime_type: Optional[str] = None

    @field_validator("path")
    def validate_path(cls, v: Any) -> Path:
        p = Path(v).expanduser().resolve()
        if not p.is_file():
            raise ValueError(f"Attachment file does not exist or is not a file: {p}")
        return p

class EmailMessage(BaseModel):
    """Complete email payload for dispatch across Outlook or Gmail."""
    subject: str = Field(..., min_length=1)
    body_html: str = Field(..., min_length=1)
    body_text: Optional[str] = None
    recipients: List[Recipient] = Field(default_factory=list)
    attachments: List[Attachment] = Field(default_factory=list)
    sender: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def add_to(self, email: str, name: Optional[str] = None) -> "EmailMessage":
        self.recipients.append(Recipient(email=email, name=name, role=RecipientRole.TO))
        return self

    def add_cc(self, email: str, name: Optional[str] = None) -> "EmailMessage":
        self.recipients.append(Recipient(email=email, name=name, role=RecipientRole.CC))
        return self

    def add_bcc(self, email: str, name: Optional[str] = None) -> "EmailMessage":
        self.recipients.append(Recipient(email=email, name=name, role=RecipientRole.BCC))
        return self

    def add_attachment(self, file_path: str) -> "EmailMessage":
        self.attachments.append(Attachment(path=Path(file_path)))
        return self

    @property
    def to_recipients(self) -> List[Recipient]:
        return [r for r in self.recipients if r.role == RecipientRole.TO]

    @property
    def cc_recipients(self) -> List[Recipient]:
        return [r for r in self.recipients if r.role == RecipientRole.CC]

    @property
    def bcc_recipients(self) -> List[Recipient]:
        return [r for r in self.recipients if r.role == RecipientRole.BCC]
