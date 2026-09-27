"""Autonomous Mail Agent Orchestrator.

High-level interface coordinating drivers, providers, sanitizers, and delivery pipelines.
Supports both Outlook and Gmail automation, fallback SMTP delivery, and CLI execution.
"""

import sys
import argparse
from typing import Optional, Dict, Any, List
from pathlib import Path

from .models import EmailMessage, Recipient, ProviderType
from .config import AgentConfig, DEFAULT_CONFIG
from .security.sanitizer import assert_payload_is_safe
from .drivers.webbridge import WebBridgeDriver
from .drivers.playwright_driver import PlaywrightDriver
from .drivers.smtp_driver import SMTPDriver
from .providers.outlook import OutlookProvider
from .providers.gmail import GmailProvider
from .exceptions import MailAgentError

class MailAgent:
    """Master orchestrator for autonomous mail operations."""

    def __init__(
        self,
        config: Optional[AgentConfig] = None,
        driver_type: str = "webbridge",
        session_name: str = "mail-agent-session"
    ):
        self.config = config or DEFAULT_CONFIG
        self.driver_type = driver_type.lower()
        self.session_name = session_name
        self.driver = self._initialize_driver()

    def _initialize_driver(self):
        """Instantiates driver based on configuration."""
        if self.driver_type == "webbridge":
            wb = WebBridgeDriver(
                daemon_url=self.config.webbridge.daemon_url,
                session=self.session_name,
                timeout=self.config.webbridge.request_timeout
            )
            return wb
        elif self.driver_type == "playwright":
            return PlaywrightDriver(headless=False)
        elif self.driver_type == "smtp":
            return SMTPDriver(smtp_host="localhost")
        else:
            raise MailAgentError(f"Unknown driver type: '{self.driver_type}'")

    def get_provider(self, provider_type: ProviderType):
        """Returns provider engine instance for the driver."""
        if provider_type == ProviderType.OUTLOOK:
            return OutlookProvider(self.driver, self.config.outlook)
        elif provider_type == ProviderType.GMAIL:
            return GmailProvider(self.driver, self.config.gmail)
        else:
            raise MailAgentError(f"Unsupported provider: '{provider_type}'")

    def dispatch(
        self,
        message: EmailMessage,
        provider_type: ProviderType = ProviderType.OUTLOOK,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """Validates, prepares, and dispatches an email message.

        Args:
            message: Populated EmailMessage object.
            provider_type: Target webmail service (OUTLOOK or GMAIL).
            dry_run: If True, populates and validates the compose dialog without clicking Send.

        Returns:
            Dict containing execution status, readiness metrics, and timestamp.
        """
        # 1. Enforce Privacy Sanitization
        if self.config.enforce_privacy_sanitization:
            assert_payload_is_safe(message.subject, message.body_html)

        # 2. Get provider
        provider = self.get_provider(provider_type)

        # 3. Open Mailbox & Compose
        provider.open_mailbox()
        provider.open_compose()

        # 4. Populate Recipients
        provider.set_recipients(message.recipients)

        # 5. Populate Subject & Body
        provider.set_subject(message.subject)
        provider.set_body(message.body_html)

        # 6. Add Attachments
        if message.attachments:
            provider.add_attachments([str(a.path) for a in message.attachments])

        # 7. Pre-flight Readiness Verification
        readiness = provider.verify_readiness()
        if not readiness.get("ready"):
            raise MailAgentError(f"Pre-flight readiness failed: {readiness}")

        result = {
            "success": True,
            "provider": provider_type.value,
            "dry_run": dry_run,
            "readiness": readiness,
            "recipient_count": len(message.recipients),
            "attachment_count": len(message.attachments)
        }

        # 8. Dispatch if not dry-run
        if not dry_run:
            provider.send()
            dispatched = provider.verify_sent()
            result["dispatched"] = dispatched

        return result

def main():
    """CLI entrypoint for auto-mail agent."""
    parser = argparse.ArgumentParser(description="Autonomous Mail Agent CLI")
    parser.add_argument("--to", action="append", required=True, help="Recipient email address (can specify multiple)")
    parser.add_argument("--cc", action="append", default=[], help="Cc email address")
    parser.add_argument("--subject", required=True, help="Email subject line")
    parser.add_argument("--body", required=True, help="Email body (HTML or plain text)")
    parser.add_argument("--provider", choices=["outlook", "gmail"], default="outlook", help="Target mail provider")
    parser.add_argument("--dry-run", action="store_true", help="Populate fields without clicking Send")
    parser.add_argument("--driver", choices=["webbridge", "playwright"], default="webbridge", help="Automation driver")
    parser.add_argument("--session", default="mail-cross-verify", help="WebBridge session name (default: mail-cross-verify)")

    args = parser.parse_args()

    agent = MailAgent(driver_type=args.driver, session_name=args.session)
    msg = EmailMessage(subject=args.subject, body_html=args.body)
    for t in args.to:
        msg.add_to(t)
    for c in args.cc:
        msg.add_cc(c)

    print(f"🚀 Dispatching email via {args.provider.upper()} ({args.driver})...")
    res = agent.dispatch(msg, provider_type=ProviderType(args.provider), dry_run=args.dry_run)
    print(f"✅ Finished: {res}")

if __name__ == "__main__":
    main()
