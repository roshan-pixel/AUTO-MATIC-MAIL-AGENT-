"""Diagnostic script to verify Outlook validPill and Gmail chip creation.

Validates that recipient email addresses are cleanly tokenized into native
interactive badges (pills without invalidPill red borders in Outlook, chips in Gmail)
via Chrome DevTools Protocol (CDP) and DOM event dispatching.
"""

import sys
import argparse
from pathlib import Path
from typing import List, Optional, Dict, Any

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from auto_mail.drivers.webbridge import WebBridgeDriver
from auto_mail.drivers.playwright_driver import PlaywrightDriver
from auto_mail.providers.outlook import OutlookProvider
from auto_mail.providers.gmail import GmailProvider
from auto_mail.models import Recipient, RecipientRole
from auto_mail.exceptions import DriverConnectionError, MailAgentError

# Instruct pytest not to collect this standalone diagnostic runner
__test__ = False

DEFAULT_OUTLOOK_RECIPIENTS = [
    Recipient(email="support@heroku.com", role=RecipientRole.TO),
    Recipient(email="marc.benioff@salesforce.com", role=RecipientRole.TO),
    Recipient(email="consumer-helpline@nic.in", role=RecipientRole.CC)
]

DEFAULT_GMAIL_RECIPIENTS = [
    Recipient(email="education@github.com", role=RecipientRole.TO),
    Recipient(email="support@github.com", role=RecipientRole.TO),
    Recipient(email="consumer-helpline@nic.in", role=RecipientRole.CC)
]

def get_driver(driver_type: str, session: str):
    """Instantiates the requested automation driver."""
    if driver_type == "webbridge":
        driver = WebBridgeDriver(session=session)
        driver.check_connection()
        return driver
    elif driver_type == "playwright":
        driver = PlaywrightDriver(headless=False)
        driver.start()
        return driver
    else:
        raise ValueError(f"Unsupported driver: '{driver_type}'")

def test_outlook_pills(
    driver=None,
    session: str = "mail-heroku-support",
    recipients: Optional[List[Recipient]] = None
) -> Dict[str, Any]:
    """Tests Outlook Web recipient pill creation and checks for red invalidPills."""
    print("\n" + "=" * 60)
    print("🔬 OUTLOOK PILL VALIDATION TEST")
    print("=" * 60)

    if driver is None:
        driver = get_driver("webbridge", session=session)

    provider = OutlookProvider(driver)
    recipients = recipients or DEFAULT_OUTLOOK_RECIPIENTS

    print(f"[*] Navigating to Outlook mailbox (session: {session})...")
    provider.open_mailbox()

    print("[*] Opening compose window...")
    provider.open_compose()

    print(f"[*] Inserting {len(recipients)} recipients into To/Cc fields...")
    for r in recipients:
        print(f"    -> [{r.role.value.upper()}] {r.email}")

    provider.set_recipients(recipients)

    print("[*] Inspecting DOM for personaPill / validPill / invalidPill elements...")
    status = provider.verify_readiness()

    valid_count = status.get("validPillCount", 0)
    invalid_count = status.get("invalidPillCount", 0)
    invalid_pills = status.get("invalidPills", [])
    valid_pills = status.get("validPills", [])

    print(f"\n📊 Diagnostics:")
    print(f"    - Valid Pills Detected  : {valid_count}")
    print(f"    - Invalid Pills Detected: {invalid_count}")
    if valid_pills:
        print(f"    - Resolved Pills        : {', '.join(valid_pills)}")
    if invalid_pills:
        print(f"    - ⚠️ Invalid List        : {', '.join(invalid_pills)}")

    passed = (invalid_count == 0 and valid_count >= len(recipients))
    if passed:
        print("\n✅ SUCCESS: All recipients resolved into valid pills without red borders!")
    elif invalid_count == 0 and valid_count > 0:
        print(f"\n⚠️ PARTIAL: {valid_count}/{len(recipients)} pills resolved, 0 invalid pills.")
    else:
        print(f"\n❌ FAILURE: Found {invalid_count} invalid pills with red borders.")

    return {
        "provider": "outlook",
        "passed": passed,
        "valid_count": valid_count,
        "invalid_count": invalid_count,
        "recipients_tested": len(recipients),
        "details": status
    }

def test_gmail_chips(
    driver=None,
    session: str = "mail-gmail-support",
    recipients: Optional[List[Recipient]] = None
) -> Dict[str, Any]:
    """Tests Gmail recipient chip creation and validates native chip tokenization."""
    print("\n" + "=" * 60)
    print("🔬 GMAIL RECIPIENT CHIP VALIDATION TEST")
    print("=" * 60)

    if driver is None:
        driver = get_driver("webbridge", session=session)

    provider = GmailProvider(driver)
    recipients = recipients or DEFAULT_GMAIL_RECIPIENTS

    print(f"[*] Navigating to Gmail mailbox (session: {session})...")
    provider.open_mailbox()

    print("[*] Opening compose dialog...")
    provider.open_compose()

    print(f"[*] Inserting {len(recipients)} recipients into To/Cc fields...")
    for r in recipients:
        print(f"    -> [{r.role.value.upper()}] {r.email}")

    provider.set_recipients(recipients)

    print("[*] Inspecting DOM for native Gmail recipient chips...")
    status = provider.verify_readiness()

    chip_count = status.get("recipientChipCount", 0)
    chips = status.get("chips", [])

    print(f"\n📊 Diagnostics:")
    print(f"    - Recipient Chips Detected: {chip_count}")
    if chips:
        print(f"    - Resolved Chips          : {', '.join(chips)}")

    passed = (chip_count >= len(recipients))
    if passed:
        print(f"\n✅ SUCCESS: All {chip_count} recipients successfully tokenized into Gmail chips!")
    else:
        print(f"\n❌ WARNING: Expected {len(recipients)} chips, but found {chip_count}.")

    return {
        "provider": "gmail",
        "passed": passed,
        "chip_count": chip_count,
        "recipients_tested": len(recipients),
        "details": status
    }

def print_summary(results: List[Dict[str, Any]]):
    """Prints a structured summary table of all test runs."""
    print("\n" + "=" * 60)
    print("📋 SUMMARY DIAGNOSTIC REPORT")
    print("=" * 60)
    all_passed = True
    for r in results:
        status_icon = "✅ PASS" if r.get("passed") else "❌ FAIL"
        if not r.get("passed"):
            all_passed = False
        provider = r.get("provider", "unknown").upper()
        tested = r.get("recipients_tested", 0)
        valid = r.get("valid_count", r.get("chip_count", 0))
        print(f"[{status_icon}] {provider:<10} | Tested: {tested} | Resolved: {valid}")
    print("=" * 60)
    return all_passed

def main():
    parser = argparse.ArgumentParser(description="Diagnostic test for Outlook pills and Gmail chips")
    parser.add_argument(
        "--provider",
        choices=["outlook", "gmail", "all"],
        default="outlook",
        help="Provider to test (default: outlook)"
    )
    parser.add_argument(
        "--driver",
        choices=["webbridge", "playwright"],
        default="webbridge",
        help="Browser driver to use (default: webbridge)"
    )
    parser.add_argument(
        "--session",
        default=None,
        help="Custom WebBridge session name"
    )
    parser.add_argument(
        "--to",
        action="append",
        help="Custom To email address (can specify multiple)"
    )
    parser.add_argument(
        "--cc",
        action="append",
        help="Custom Cc email address (can specify multiple)"
    )

    args = parser.parse_args()

    # Build custom recipients if provided
    custom_recipients = None
    if args.to or args.cc:
        custom_recipients = []
        for t in (args.to or []):
            custom_recipients.append(Recipient(email=t, role=RecipientRole.TO))
        for c in (args.cc or []):
            custom_recipients.append(Recipient(email=c, role=RecipientRole.CC))

    results = []

    try:
        if args.provider in ("outlook", "all"):
            session = args.session or "mail-heroku-support"
            driver = get_driver(args.driver, session)
            res = test_outlook_pills(driver=driver, session=session, recipients=custom_recipients)
            results.append(res)

        if args.provider in ("gmail", "all"):
            session = args.session or "mail-gmail-support"
            driver = get_driver(args.driver, session)
            res = test_gmail_chips(driver=driver, session=session, recipients=custom_recipients)
            results.append(res)

        all_ok = print_summary(results)
        sys.exit(0 if all_ok else 1)

    except DriverConnectionError as e:
        print(f"\n❌ Driver Connection Error: {e}")
        print("💡 Ensure Kimi WebBridge daemon is running at http://127.0.0.1:10086 and browser extension is active.")
        sys.exit(2)
    except Exception as e:
        print(f"\n❌ Unexpected error during diagnostic: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
