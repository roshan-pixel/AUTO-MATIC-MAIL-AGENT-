"""Example: Sending a Developer Notice via Google Gmail Web."""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from auto_mail.agent import MailAgent
from auto_mail.models import EmailMessage, ProviderType

def run():
    print("=" * 70)
    print("AUTONOMOUS GMAIL NOTICE DISPATCH")
    print("=" * 70)

    msg = EmailMessage(
        subject="Student Developer Verification & Open-Source Cloud Deployment Status",
        body_html="""<div>Dear Support & Academic Alliances Team,<br><br>
This is an automated notification regarding the cloud deployment status of the open-source
accounting ledger system (<b>Ledger Web</b>) deployed to custom domain <b>https://dsr7.me</b>.<br><br>
• Developer: Roshan Rathore (<a href="https://github.com/roshan-pixel">roshan-pixel</a>)<br>
• Source Repository: <a href="https://github.com/roshan-pixel/-ledger_web">https://github.com/roshan-pixel/-ledger_web</a><br>
• Jurisdictions: India & Singapore<br><br>
Please verify the linked developer credits.<br><br>
Sincerely,<br>
<b>Roshan Rathore</b></div>"""
    )

    msg.add_to("education@github.com")
    msg.add_cc("consumer-helpline@nic.in")

    agent = MailAgent(driver_type="webbridge", session_name="mail-gmail-support")
    print("[*] Dispatching via Gmail Web Provider (dry-run mode)...")

    result = agent.dispatch(msg, provider_type=ProviderType.GMAIL, dry_run=True)
    print("\n[+] Gmail Pre-flight Readiness:")
    print(f"    - Recipient Chips: {result['readiness'].get('recipientChipCount')}")
    print(f"    - Subject Set: {result['readiness'].get('subjectSet')}")
    print(f"    - Body Set: {result['readiness'].get('bodySet')}")
    print(f"\n[+] Status: {'SUCCESS' if result.get('success') else 'FAILED'}")

if __name__ == "__main__":
    run()
