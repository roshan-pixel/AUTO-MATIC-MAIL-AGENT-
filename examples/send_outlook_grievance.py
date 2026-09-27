"""Example: Sending a Formal Dual-Jurisdiction Legal Grievance via Outlook Web."""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from auto_mail.agent import MailAgent
from auto_mail.models import EmailMessage, ProviderType
from auto_mail.templates.legal_grievance import generate_dual_jurisdiction_grievance

def run():
    print("=" * 70)
    print("AUTONOMOUS OUTLOOK GRIEVANCE DISPATCH (DUAL JURISDICTION)")
    print("=" * 70)

    # 1. Generate statutory complaint payload
    payload = generate_dual_jurisdiction_grievance(
        claimant_name="Roshan Rathore",
        registered_email="sgarmy200@outlook.com",
        github_user="roshan-pixel",
        target_platform="Heroku / Salesforce Inc.",
        advertised_offer="$13 USD credit per month for 24 months via GitHub Student Developer Pack",
        error_experienced='Gateway Address Validation Failure ("Unable to recognize city")',
        charge_amount="USD $1.00 (equivalent to INR ₹95.55)",
        merchant_descriptor="WWW-HEROKUCHARGE-COM",
        project_repo="https://github.com/roshan-pixel/-ledger_web",
        production_domain="dsr7.me"
    )

    msg = EmailMessage(
        subject=payload["subject"],
        body_html=payload["body_html"]
    )

    # 2. Add recipients (Heroku, Salesforce, GitHub, Regulators)
    recipients_to = [
        "support@heroku.com",
        "help@heroku.com",
        "legal@heroku.com",
        "security@heroku.com",
        "legal@salesforce.com",
        "privacy@salesforce.com",
        "compliance@salesforce.com",
        "executivesupport@salesforce.com",
        "marc.benioff@salesforce.com",
    ]
    for r in recipients_to:
        msg.add_to(r)

    recipients_cc = [
        "education@github.com",
        "support@github.com",
        "consumer-helpline@nic.in",
        "cp-ccpa@gov.in",
        "crpc@rbi.org.in",
        "complaints@case.org.sg",
        "cccs_feedback@cccs.gov.sg",
        "consumers@mas.gov.sg",
        "customercare@dcbbank.com",
        "grievance@dcbbank.com"
    ]
    for c in recipients_cc:
        msg.add_cc(c)

    # 3. Instantiate Agent and Dispatch
    agent = MailAgent(driver_type="webbridge", session_name="mail-heroku-support")
    print(f"[*] Prepared message with {len(msg.to_recipients)} TO and {len(msg.cc_recipients)} CC recipients.")
    print("[*] Dispatching via Outlook Web Provider...")

    # Set dry_run=True to inspect the compose pane before clicking send
    result = agent.dispatch(msg, provider_type=ProviderType.OUTLOOK, dry_run=True)
    print("\n[+] Pre-flight Readiness:")
    print(f"    - Valid Pills: {result['readiness'].get('validPillCount')}")
    print(f"    - Invalid Pills: {result['readiness'].get('invalidPillCount')}")
    print(f"    - Subject Set: {result['readiness'].get('subjectSet')}")
    print(f"    - Body Set: {result['readiness'].get('bodySet')}")
    print(f"\n[+] Status: {'SUCCESS' if result.get('success') else 'FAILED'}")

if __name__ == "__main__":
    run()
