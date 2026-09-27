"""Example: Unified multi-provider dispatch pattern."""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from auto_mail.agent import MailAgent
from auto_mail.models import EmailMessage, ProviderType

def send_alert_to_both(provider_choice: str = "outlook"):
    msg = EmailMessage(
        subject="Automated Developer Notification | Infrastructure Status",
        body_html="<p>This alert is dispatched uniformly across Outlook and Gmail.</p>"
    )
    msg.add_to("support@heroku.com")
    msg.add_cc("education@github.com")

    agent = MailAgent(driver_type="webbridge")
    provider = ProviderType.OUTLOOK if provider_choice == "outlook" else ProviderType.GMAIL
    res = agent.dispatch(msg, provider_type=provider, dry_run=True)
    print(f"Result for {provider_choice}: {res}")

if __name__ == "__main__":
    choice = sys.argv[1] if len(sys.argv) > 1 else "outlook"
    send_alert_to_both(choice)
