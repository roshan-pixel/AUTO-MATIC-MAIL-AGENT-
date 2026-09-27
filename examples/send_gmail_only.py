"""
Focused Gmail → Outlook send script.
Sends from sgarmy200@gmail.com → sgarmy200@outlook.com.
Takes a screenshot after composing for visual confirmation.
"""
import sys
import time
from pathlib import Path
sys.path.insert(0, r"C:\Users\sgarm\AUTO-MATIC-MAIL-AGENT-")

from auto_mail.drivers.webbridge import WebBridgeDriver
from auto_mail.providers.gmail import GmailProvider
from auto_mail.config import GmailSelectors
from auto_mail.models import EmailMessage, Recipient, RecipientRole

# ── Configuration ────────────────────────────────────────────────────────────
WEBBRIDGE_URL = "http://127.0.0.1:10086"
SESSION_NAME  = "mail-cross-verify"

TO_EMAIL   = "sgarmy200@outlook.com"
SUBJECT    = "Cross-Verify Test: Gmail → Outlook ✉"
BODY_HTML  = (
    "<p>Hi,</p>"
    "<p>This is a cross-verification test email sent via <strong>AUTO-MATIC-MAIL-AGENT</strong> "
    "from <strong>sgarmy200@gmail.com</strong> to <strong>sgarmy200@outlook.com</strong>.</p>"
    "<p>If you received this, Phase 2 is confirmed ✓</p>"
)

SCREENSHOT_PATH = Path(r"C:\Users\sgarm\AUTO-MATIC-MAIL-AGENT-\examples\gmail_compose_preview.png")

# ── Setup driver ──────────────────────────────────────────────────────────────
print("=" * 60)
print("  Gmail → Outlook · AUTO-MATIC-MAIL-AGENT")
print("=" * 60)

driver = WebBridgeDriver(daemon_url=WEBBRIDGE_URL, session=SESSION_NAME)

print("[0/7] Checking WebBridge connection...")
try:
    status = driver.check_connection()
    print(f"      ✓ daemon running, extension connected, version={status.get('version','?')}")
except Exception as e:
    print(f"      ✗ WebBridge error: {e}")
    sys.exit(1)

# ── Verify Gmail is open ──────────────────────────────────────────────────────
print("\n[1/7] Verifying Gmail tab is active (sgarmy200@gmail.com)...")
# Quick JS check — reads which Gmail account is open
account_check = """(() => {
    const meta = document.querySelector('meta[name="application-name"]');
    const title = document.title || '';
    const url = location.href;
    return { title, url };
})()"""
page_info = driver.evaluate(account_check)
print(f"      Current page: {page_info}")

if page_info and "google" not in str(page_info.get("url", "")).lower():
    print("\n[!] Not on Gmail! Navigating to Gmail...")
    driver.navigate("https://mail.google.com/mail/u/0/#inbox")
    time.sleep(2.0)
else:
    print("      ✓ Gmail tab detected")

# ── Open compose ──────────────────────────────────────────────────────────────
provider = GmailProvider(driver, GmailSelectors())

print("[2/7] Opening Gmail compose pane...")
provider.open_compose(timeout_sec=20.0)
print("      ✓ Compose pane opened")
time.sleep(0.6)

# ── Set recipient ─────────────────────────────────────────────────────────────
print(f"[3/7] Setting recipient → {TO_EMAIL}")
msg = EmailMessage(
    subject=SUBJECT,
    body_html=BODY_HTML,
    recipients=[Recipient(email=TO_EMAIL, role=RecipientRole.TO)],
)
provider.set_recipients(msg.recipients)
print("      ✓ Recipient set")
time.sleep(0.4)

# ── Set subject ───────────────────────────────────────────────────────────────
print(f"[4/7] Setting subject → {SUBJECT!r}")
provider.set_subject(SUBJECT)
print("      ✓ Subject set")

# ── Set body ──────────────────────────────────────────────────────────────────
print("[5/7] Setting email body...")
provider.set_body(BODY_HTML)
print("      ✓ Body set")
time.sleep(0.5)

# ── Screenshot BEFORE send ────────────────────────────────────────────────────
print("[6/7] Taking screenshot to confirm compose state...")
try:
    shot = driver.take_screenshot(SCREENSHOT_PATH)
    print(f"      📸 Screenshot saved → {shot}")
except Exception as e:
    print(f"      Screenshot failed (non-fatal): {e}")

# ── Readiness check ───────────────────────────────────────────────────────────
print("\n[CHECK] Readiness report:")
readiness = provider.verify_readiness()
for k, v in readiness.items():
    print(f"        {k}: {v}")

if not readiness.get("subjectSet"):
    print("\n⚠️  Subject NOT set — aborting to avoid sending blank-subject email.")
    sys.exit(1)

if not readiness.get("bodySet"):
    print("\n⚠️  Body NOT set — aborting.")
    sys.exit(1)

if not readiness.get("chipsReady"):
    print(f"\n⚠️  Recipient chip NOT committed (recipientChipCount=0). Aborting.")
    sys.exit(1)

# ── Send ───────────────────────────────────────────────────────────────────────
print("\n[7/7] Sending email via Ctrl+Enter...")
provider.send()
print("      ✓ Send dispatched")

time.sleep(2.0)

# ── Post-send verification ────────────────────────────────────────────────────
sent = provider.verify_sent(timeout_sec=12.0)
if sent:
    print("\n✅  SENT — 'Message sent' toast detected or compose closed.")
else:
    print("\n⚠️  Could not confirm toast within 12s — email may still have been sent.")
    print("    Check Gmail Sent folder and sgarmy200@outlook.com inbox.")

print("\n" + "=" * 60)
print("  Done. Check sgarmy200@outlook.com for the email!")
print("=" * 60)
