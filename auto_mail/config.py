"""Configuration management for Auto-Matic-Mail-Agent."""

from pathlib import Path
from pydantic import BaseModel, Field

class WebBridgeConfig(BaseModel):
    """Configuration for Kimi WebBridge daemon."""
    daemon_url: str = "http://127.0.0.1:10086"
    command_endpoint: str = "/command"
    status_endpoint: str = "/status"
    default_session: str = "mail-agent-session"
    request_timeout: float = 30.0

class OutlookSelectors(BaseModel):
    """DOM selectors for Microsoft Outlook Web (live.com / office.com)."""
    new_mail_button: str = 'button[aria-label*="New mail"], button[name="New mail"], [data-item-id="newMessage"]'
    to_field: str = 'div[aria-label="To"], input[aria-label="To"], [aria-label*="To recipient"]'
    cc_button: str = 'button[aria-label*="Cc"], button[name="Cc"], span:has-text("Cc")'
    cc_field: str = 'div[aria-label="Cc"], input[aria-label="Cc"], [aria-label*="Cc recipient"]'
    bcc_button: str = 'button[aria-label*="Bcc"], button[name="Bcc"]'
    bcc_field: str = 'div[aria-label="Bcc"], input[aria-label="Bcc"]'
    subject_field: str = 'input[placeholder="Add a subject"], [aria-label="Subject"], input[aria-label*="Subject"]'
    body_field: str = 'div[aria-label="Message body"], div[role="textbox"][contenteditable="true"]'
    send_button: str = 'button[aria-label*="Send"], button[title*="Send (Ctrl+Enter)"]'
    pill_container: str = '[class*="personaPill"], [class*="validPill"], [class*="invalidPill"], [data-log-name="PersonaPill"], div[class*="pickerItem"], span[class*="personaPill"]'
    invalid_pill: str = '[class*="invalidPill"], [class*="errorPill"], [aria-invalid="true"]'
    attachment_input: str = 'input[type="file"]'

class GmailSelectors(BaseModel):
    """DOM selectors for Google Gmail Web."""
    compose_button: str = 'div[role="button"][gh="cm"], div[aria-label*="Compose"], .T-I.T-I-KE.L3'
    to_field: str = 'input[role="combobox"][aria-label*="To"], input[aria-label*="Search for people"], div[name="to"] input'
    cc_button: str = 'span[role="link"][data-tooltip*="Add Cc"], span[aria-label*="Add Cc"]'
    cc_field: str = 'input[role="combobox"][aria-label*="Cc"], div[name="cc"] input'
    bcc_button: str = 'span[role="link"][data-tooltip*="Add Bcc"], span[aria-label*="Add Bcc"]'
    bcc_field: str = 'input[role="combobox"][aria-label*="Bcc"], div[name="bcc"] input'
    subject_field: str = 'input[name="subjectbox"], input[placeholder="Subject"], input[aria-label="Subject"]'
    body_field: str = 'div[aria-label="Message Body"][contenteditable="true"], div[role="textbox"][contenteditable="true"]'
    send_button: str = 'div[role="button"][data-tooltip*="Send"], div[aria-label*="Send ‪(Ctrl-Enter)‬"]'
    attachment_button: str = 'div[command="Files"], div[aria-label*="Attach files"]'
    attachment_input: str = 'input[type="file"][name="Filedata"]'
    chip_container: str = 'div[data-hovercard-id], span[email], div[role="option"], div.vR, span.vN'

class AgentConfig(BaseModel):
    """Global configuration settings for Mail Agent."""
    webbridge: WebBridgeConfig = Field(default_factory=WebBridgeConfig)
    outlook: OutlookSelectors = Field(default_factory=OutlookSelectors)
    gmail: GmailSelectors = Field(default_factory=GmailSelectors)
    typing_delay_sec: float = 0.05
    event_settle_delay_sec: float = 0.2
    max_retries: int = 3
    enforce_privacy_sanitization: bool = True
    auto_capture_screenshots: bool = True
    screenshot_dir: Path = Field(default_factory=lambda: Path.home() / ".auto_mail" / "screenshots")

DEFAULT_CONFIG = AgentConfig()
