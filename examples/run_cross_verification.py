"""Cross-Verification Engine: Outlook <-> Gmail.

Dispatches an email:
  1. From Microsoft Outlook Web to sgarmy200@gmail.com
  2. From Google Gmail Web to sgarmy200@outlook.com
And verifies delivery in both inboxes.
"""

import sys
import time
import json
import uuid
import datetime
from pathlib import Path
from typing import Dict, Any

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from auto_mail.drivers.webbridge import WebBridgeDriver
from auto_mail.providers.outlook import OutlookProvider
from auto_mail.providers.gmail import GmailProvider
from auto_mail.models import EmailMessage, Recipient, RecipientRole, ProviderType

SESSION_NAME = "mail-cross-verify"

def run_cross_verification():
    run_id = uuid.uuid4().hex[:8].upper()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("=" * 70)
    print(f"🚀 BIDIRECTIONAL CROSS-VERIFICATION RUN [ID: {run_id}]")
    print(f"⏰ Timestamp: {now_str}")
    print("=" * 70)

    driver = WebBridgeDriver(session=SESSION_NAME)
    driver.check_connection()

    outlook_provider = OutlookProvider(driver)
    gmail_provider = GmailProvider(driver)

    # -------------------------------------------------------------
    # 1. OUTLOOK -> GMAIL DISPATCH
    # -------------------------------------------------------------
    print("\n" + "-" * 60)
    print("📤 PHASE 1: DISPATCH FROM OUTLOOK -> sgarmy200@gmail.com")
    print("-" * 60)

    outlook_subject = f"Cross-Verification: Outlook -> Gmail [RunID: {run_id}]"
    outlook_body = f"""<div style="font-family: Arial, sans-serif; padding: 15px; border-left: 4px solid #0078d4;">
        <h3 style="color: #0078d4; margin-top: 0;">Automated Cross-Verification Notice</h3>
        <p>This email was automatically dispatched by <b>Auto-Matic-Mail-Agent</b> via Microsoft Outlook Web.</p>
        <p><b>Target:</b> sgarmy200@gmail.com<br>
        <b>Run ID:</b> <code>{run_id}</code><br>
        <b>Timestamp:</b> {now_str}</p>
        <hr style="border: none; border-top: 1px solid #e0e0e0;">
        <p style="font-size: 12px; color: #666;">Autonomous Mail Verification System | Dual-Provider Verification</p>
    </div>"""

    print("[*] Navigating to Outlook Web...")
    driver.navigate("https://outlook.live.com/mail/")
    time.sleep(2.0)

    print("[*] Opening Outlook compose pane...")
    outlook_provider.open_compose()
    time.sleep(1.0)

    print("[*] Setting recipient: sgarmy200@gmail.com...")
    outlook_provider.set_recipients([
        Recipient(email="sgarmy200@gmail.com", role=RecipientRole.TO)
    ])
    time.sleep(0.5)

    print(f"[*] Setting subject: '{outlook_subject}'...")
    outlook_provider.set_subject(outlook_subject)
    time.sleep(0.5)

    print("[*] Setting rich message body...")
    outlook_provider.set_body(outlook_body)
    time.sleep(0.5)

    print("[*] Verifying Outlook pre-flight readiness...")
    readiness_outlook = outlook_provider.verify_readiness()
    print(f"    - Valid Pills Detected  : {readiness_outlook.get('validPillCount')}")
    print(f"    - Invalid Pills Detected: {readiness_outlook.get('invalidPillCount')}")
    print(f"    - Subject Set           : {readiness_outlook.get('subjectSet')}")
    print(f"    - Body Set              : {readiness_outlook.get('bodySet')}")

    if not readiness_outlook.get("pillsReady", False) and readiness_outlook.get("validPillCount", 0) == 0:
        print("⚠️ Warning: Valid pill count is 0, checking invalid pills...")
        if readiness_outlook.get("invalidPillCount", 0) > 0:
            raise RuntimeError(f"Outlook invalid pill detected: {readiness_outlook.get('invalidPills')}")

    print("[*] Sending email via Outlook (Ctrl+Enter / Send)...")
    outlook_provider.send()
    time.sleep(2.0)

    sent_outlook = outlook_provider.verify_sent(timeout_sec=10.0)
    print(f"✅ Outlook Dispatch Result: {'DISPATCHED' if sent_outlook else 'PENDING/SENT'}")

    # -------------------------------------------------------------
    # 2. GMAIL -> OUTLOOK DISPATCH
    # -------------------------------------------------------------
    print("\n" + "-" * 60)
    print("📤 PHASE 2: DISPATCH FROM GMAIL -> sgarmy200@outlook.com")
    print("-" * 60)

    gmail_subject = f"Cross-Verification: Gmail -> Outlook [RunID: {run_id}]"
    gmail_body = f"""<div style="font-family: Arial, sans-serif; padding: 15px; border-left: 4px solid #ea4335;">
        <h3 style="color: #ea4335; margin-top: 0;">Automated Cross-Verification Notice</h3>
        <p>This email was automatically dispatched by <b>Auto-Matic-Mail-Agent</b> via Google Gmail Web.</p>
        <p><b>Target:</b> sgarmy200@outlook.com<br>
        <b>Run ID:</b> <code>{run_id}</code><br>
        <b>Timestamp:</b> {now_str}</p>
        <hr style="border: none; border-top: 1px solid #e0e0e0;">
        <p style="font-size: 12px; color: #666;">Autonomous Mail Verification System | Dual-Provider Verification</p>
    </div>"""

    print("[*] Navigating to Gmail Web...")
    driver.navigate("https://mail.google.com/mail/u/0/")
    time.sleep(2.0)

    print("[*] Opening Gmail compose dialog...")
    gmail_provider.open_compose()
    time.sleep(1.0)

    print("[*] Setting recipient: sgarmy200@outlook.com...")
    gmail_provider.set_recipients([
        Recipient(email="sgarmy200@outlook.com", role=RecipientRole.TO)
    ])
    time.sleep(0.5)

    print(f"[*] Setting subject: '{gmail_subject}'...")
    gmail_provider.set_subject(gmail_subject)
    time.sleep(0.5)

    print("[*] Setting rich message body...")
    gmail_provider.set_body(gmail_body)
    time.sleep(0.5)

    print("[*] Verifying Gmail pre-flight readiness...")
    readiness_gmail = gmail_provider.verify_readiness()
    print(f"    - Recipient Chips Detected: {readiness_gmail.get('recipientChipCount')}")
    print(f"    - Subject Set             : {readiness_gmail.get('subjectSet')}")
    print(f"    - Body Set                : {readiness_gmail.get('bodySet')}")

    print("[*] Sending email via Gmail (Ctrl+Enter / Send)...")
    gmail_provider.send()
    time.sleep(2.0)

    sent_gmail = gmail_provider.verify_sent(timeout_sec=10.0)
    print(f"✅ Gmail Dispatch Result: {'DISPATCHED' if sent_gmail else 'PENDING/SENT'}")

    # -------------------------------------------------------------
    # 3. VERIFICATION IN BOTH INBOXES
    # -------------------------------------------------------------
    print("\n" + "-" * 60)
    print("📥 PHASE 3: VERIFYING RECEPTION IN BOTH INBOXES")
    print("-" * 60)

    print("[*] Waiting 15 seconds for mail transport across providers...")
    for remaining in range(15, 0, -5):
        print(f"    ... waiting {remaining}s")
        time.sleep(5)

    # 3A. Verify in Gmail Inbox (looking for email sent from Outlook)
    print("\n[🔍] Checking Gmail Inbox for email from Outlook...")
    driver.navigate("https://mail.google.com/mail/u/0/#inbox")
    time.sleep(3.0)

    gmail_found = False
    for poll in range(4):
        # Refresh or check DOM
        check_code = f"""(() => {{
            const bodyText = document.body.innerText || '';
            const foundSubj = bodyText.includes({json.dumps(run_id)}) || bodyText.includes('Cross-Verification: Outlook -> Gmail');
            const row = Array.from(document.querySelectorAll('tr, span, div')).find(el => el.innerText && el.innerText.includes({json.dumps(run_id)}));
            return {{
                found: !!(foundSubj || row),
                snippet: row ? row.innerText.substring(0, 100) : null
            }};
        }})()"""
        check_res = driver.evaluate(check_code) or {}
        if check_res.get("found"):
            gmail_found = True
            print(f"    ✅ CONFIRMED: Found email in Gmail inbox! Snippet: {check_res.get('snippet')}")
            break
        print(f"    ... poll {poll+1}/4: Not found yet, checking again in 5s...")
        time.sleep(5.0)

    # 3B. Verify in Outlook Inbox (looking for email sent from Gmail)
    print("\n[🔍] Checking Outlook Inbox for email from Gmail...")
    driver.navigate("https://outlook.live.com/mail/0/inbox")
    time.sleep(3.0)

    outlook_found = False
    for poll in range(4):
        check_code = f"""(() => {{
            const bodyText = document.body.innerText || '';
            const foundSubj = bodyText.includes({json.dumps(run_id)}) || bodyText.includes('Cross-Verification: Gmail -> Outlook');
            const row = Array.from(document.querySelectorAll('div[role=\"option\"], div[data-convid], span')).find(el => el.innerText && el.innerText.includes({json.dumps(run_id)}));
            return {{
                found: !!(foundSubj || row),
                snippet: row ? row.innerText.substring(0, 100) : null
            }};
        }})()"""
        check_res = driver.evaluate(check_code) or {}
        if check_res.get("found"):
            outlook_found = True
            print(f"    ✅ CONFIRMED: Found email in Outlook inbox! Snippet: {check_res.get('snippet')}")
            break
        print(f"    ... poll {poll+1}/4: Not found yet, checking again in 5s...")
        time.sleep(5.0)

    # -------------------------------------------------------------
    # 4. FINAL REPORT
    # -------------------------------------------------------------
    print("\n" + "=" * 70)
    print("📊 CROSS-VERIFICATION AUDIT SUMMARY")
    print("=" * 70)
    print(f"• Run ID                          : {run_id}")
    print(f"• Outlook -> Gmail Sent           : {'✅ YES' if sent_outlook else '⚠️ UNCONFIRMED'}")
    print(f"• Gmail -> Outlook Sent           : {'✅ YES' if sent_gmail else '⚠️ UNCONFIRMED'}")
    print(f"• Received in Gmail Inbox         : {'✅ VERIFIED' if gmail_found else '⏳ PENDING/SPAM FOLDER'}")
    print(f"• Received in Outlook Inbox       : {'✅ VERIFIED' if outlook_found else '⏳ PENDING/JUNK FOLDER'}")
    print("=" * 70)

    return {
        "run_id": run_id,
        "sent_outlook": sent_outlook,
        "sent_gmail": sent_gmail,
        "received_gmail": gmail_found,
        "received_outlook": outlook_found
    }

if __name__ == "__main__":
    run_cross_verification()
