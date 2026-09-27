"""
Focused Outlook → Gmail send script.
Sends from sgarmy200@outlook.com → sgarmy200@gmail.com.
Takes a screenshot after composing so you can visually confirm everything.
"""
import sys
import time
from pathlib import Path
sys.path.insert(0, r"C:\Users\sgarm\AUTO-MATIC-MAIL-AGENT-")

from auto_mail.drivers.webbridge import WebBridgeDriver
from auto_mail.providers.outlook import OutlookProvider
from auto_mail.config import OutlookSelectors
from auto_mail.models import EmailMessage, Recipient, RecipientRole

# ── Configuration ────────────────────────────────────────────────────────────
WEBBRIDGE_URL  = "http://127.0.0.1:10086"
SESSION_NAME   = "mail-cross-verify"

TO_EMAIL    = "sgarmy200@gmail.com"
SUBJECT     = "Cross-Verify Test: Outlook → Gmail ✉"
BODY_HTML   = "<p>Hi,</p><p>This is a cross-verification test email sent via AUTO-MATIC-MAIL-AGENT from <strong>sgarmy200@outlook.com</strong> to <strong>sgarmy200@gmail.com</strong>.</p><p>If you received this, Phase 1 is confirmed ✓</p>"

SCREENSHOT_PATH = Path(r"C:\Users\sgarm\AUTO-MATIC-MAIL-AGENT-\examples\compose_before_send.png")

# ── Setup driver ──────────────────────────────────────────────────────────────
print("=" * 60)
print("  Outlook → Gmail · AUTO-MATIC-MAIL-AGENT")
print("=" * 60)

driver = WebBridgeDriver(
    daemon_url=WEBBRIDGE_URL,
    session=SESSION_NAME,
)

print(f"[0/7] Checking WebBridge connection...")
try:
    status = driver.check_connection()
    print(f"      ✓ daemon running, extension connected, version={status.get('version','?')}")
except Exception as e:
    print(f"      ✗ WebBridge error: {e}")
    sys.exit(1)

# ── Open compose ──────────────────────────────────────────────────────────────
provider = OutlookProvider(driver, OutlookSelectors())

print("[1/7] Navigating to Outlook inbox...")
driver.navigate("https://outlook.live.com/mail/")
time.sleep(1.0)

print("[2/7] Opening Outlook compose pane...")
provider.open_compose(timeout_sec=20.0)
print("      Compose pane opened ✓")
time.sleep(0.8)  # Extra settle time

# ── Set recipient ─────────────────────────────────────────────────────────────
print(f"[3/7] Setting recipient → {TO_EMAIL}")
msg = EmailMessage(
    subject=SUBJECT,
    body_html=BODY_HTML,
    recipients=[Recipient(email=TO_EMAIL, role=RecipientRole.TO)],
)
provider.set_recipients(msg.recipients)
print("      Recipient set ✓")
time.sleep(0.5)

# ── Set subject ───────────────────────────────────────────────────────────────
print(f"[4/7] Setting subject → {SUBJECT!r}")
provider.set_subject(SUBJECT)
print("      Subject set ✓")

# ── Set body ──────────────────────────────────────────────────────────────────
print("[5/7] Setting email body...")
provider.set_body(BODY_HTML)
print("      Body set ✓")
time.sleep(0.5)

# ── Screenshot BEFORE send — visual confirmation ──────────────────────────────
print("[6/7] Taking screenshot to confirm compose state...")
try:
    shot = driver.take_screenshot(SCREENSHOT_PATH)
    print(f"      Screenshot saved → {shot}")
except Exception as e:
    print(f"      Screenshot failed (non-fatal): {e}")

# ── Readiness check ───────────────────────────────────────────────────────────
print("\n[CHECK] Readiness report:")
readiness = provider.verify_readiness()
for k, v in readiness.items():
    print(f"        {k}: {v}")

if not readiness.get("subjectSet"):
    print("\n⚠️  Subject STILL not set — aborting to protect you from blank-subject email.")
    print("    Screenshot saved above — check compose window manually.")
    sys.exit(1)

if not readiness.get("bodySet"):
    print("\n⚠️  Body not set — aborting.")
    sys.exit(1)

# ── Send ───────────────────────────────────────────────────────────────────────
print("\n[7/7] Sending email via Ctrl+Enter...")
provider.send()
print("      Send dispatched ✓")

time.sleep(2.0)

# ── Post-send verification ────────────────────────────────────────────────────
sent = provider.verify_sent(timeout_sec=12.0)
if sent:
    print("\n✅  SENT — compose pane closed successfully.")
else:
    print("\n⚠️  Compose pane still visible after 12s — email may still have been sent.")
    print("    Check your Outlook Sent Items and the sgarmy200@gmail.com inbox.")

print("\n" + "=" * 60)
print("  Done. Check sgarmy200@gmail.com for the email!")
print("=" * 60)
