#!/usr/bin/env python3
"""
⚡ AUTO-MATIC MAIL AGENT — One-Shot Outlook Mail Dispatcher ⚡
=============================================================
Send emails via Microsoft Outlook Web (live.com / office.com) in one go!
Supports interactive prompts, CLI arguments, attachments, and visual verification.

Usage:
  Interactive Mode:
    python send_outlook.py

  One-Line Direct CLI:
    python send_outlook.py -t sgarmy200@gmail.com -s "Hello" -b "My message" -y

  With Attachment & CC:
    python send_outlook.py -t user@example.com -c team@example.com -s "Report" -b "Attached" -a ./report.pdf -y
"""

import sys
import os
import time
import argparse
from pathlib import Path
from typing import List, Optional

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from auto_mail.drivers.webbridge import WebBridgeDriver
from auto_mail.providers.outlook import OutlookProvider
from auto_mail.config import OutlookSelectors, DEFAULT_CONFIG
from auto_mail.models import EmailMessage, Recipient, RecipientRole, EMAIL_REGEX
from auto_mail.security.sanitizer import assert_payload_is_safe


# Color helpers for terminal output
class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"


def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}╔════════════════════════════════════════════════════════════════════════╗
║             ⚡ AUTO-MATIC MAIL AGENT — OUTLOOK DISPATCH ⚡             ║
║            One-shot automated email delivery via Outlook Web           ║
╚════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)


def check_webbridge_daemon(driver: WebBridgeDriver) -> bool:
    """Verifies that the WebBridge daemon and browser extension are connected."""
    try:
        status = driver.check_connection()
        print(f" {Colors.GREEN}✓{Colors.RESET} WebBridge daemon active (v{status.get('version', '2.x')}) | Browser extension connected")
        return True
    except Exception as e:
        print(f"\n{Colors.RED}❌ WebBridge Connection Error:{Colors.RESET} {e}")
        print(f"\n{Colors.YELLOW}Troubleshooting:{Colors.RESET}")
        print("  1. Make sure Kimi WebBridge daemon is running at http://127.0.0.1:10086")
        print("  2. Ensure your Chrome/Edge browser has the WebBridge extension installed & enabled")
        print("  3. Make sure you are logged into Outlook Web (https://outlook.live.com/mail/)")
        return False


def prompt_multiline_body() -> str:
    """Collects multi-line text from user until EOF or empty line with 'END'."""
    print(f"{Colors.DIM}Enter body text. Type 'END' on a new line or press Ctrl+Z / Ctrl+D when finished:{Colors.RESET}")
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        except EOFError:
            break
    return "\n".join(lines)


def get_interactive_inputs() -> dict:
    """Prompts the user interactively for email parameters."""
    print(f"{Colors.BOLD}Please provide the email details:{Colors.RESET}\n")

    # 1. Recipient TO
    while True:
        to_input = input(f"{Colors.CYAN}To (recipient email): {Colors.RESET}").strip()
        if not to_input:
            print(f"{Colors.RED}Recipient 'To' cannot be empty.{Colors.RESET}")
            continue
        to_list = [e.strip() for e in to_input.replace(",", " ").split() if e.strip()]
        invalid = [e for e in to_list if not EMAIL_REGEX.match(e)]
        if invalid:
            print(f"{Colors.RED}Invalid email syntax: {', '.join(invalid)}. Please try again.{Colors.RESET}")
            continue
        break

    # 2. Recipient CC
    cc_input = input(f"{Colors.CYAN}Cc (optional, press Enter to skip): {Colors.RESET}").strip()
    cc_list = [e.strip() for e in cc_input.replace(",", " ").split() if e.strip()]

    # 3. Subject
    while True:
        subject = input(f"{Colors.CYAN}Subject: {Colors.RESET}").strip()
        if subject:
            break
        print(f"{Colors.RED}Subject line is required.{Colors.RESET}")

    # 4. Body
    print(f"\n{Colors.CYAN}Body Options:{Colors.RESET}")
    print("  • Type message directly")
    print("  • Type 'MULTI' for multiline message")
    print("  • Type '@filename.txt' or '@filename.html' to load from file")
    body_input = input(f"{Colors.CYAN}Body: {Colors.RESET}").strip()

    if body_input.upper() == "MULTI":
        body = prompt_multiline_body()
    elif body_input.startswith("@"):
        file_path = Path(body_input[1:].strip())
        if file_path.is_file():
            body = file_path.read_text(encoding="utf-8")
            print(f" {Colors.GREEN}✓{Colors.RESET} Loaded {len(body)} chars from {file_path}")
        else:
            print(f"{Colors.YELLOW}File not found. Using input as plain text.{Colors.RESET}")
            body = body_input
    else:
        body = body_input

    # 5. Attachment
    att_input = input(f"\n{Colors.CYAN}Attachment file path (optional, press Enter to skip): {Colors.RESET}").strip()
    attachments = []
    if att_input:
        att_path = Path(att_input.strip("\"'"))
        if att_path.is_file():
            attachments.append(att_path)
            print(f" {Colors.GREEN}✓{Colors.RESET} Attachment verified: {att_path.name}")
        else:
            print(f" {Colors.YELLOW}⚠️  File not found at '{att_path}'. Proceeding without attachment.{Colors.RESET}")

    return {
        "to": to_list,
        "cc": cc_list,
        "subject": subject,
        "body": body,
        "attachments": attachments,
    }


def send_mail(
    to_emails: List[str],
    subject: str,
    body: str,
    cc_emails: Optional[List[str]] = None,
    attachments: Optional[List[Path]] = None,
    dry_run: bool = False,
    take_screenshot: bool = True,
    session_name: str = "mail-cross-verify",
    daemon_url: str = "http://127.0.0.1:10086",
) -> bool:
    """Executes the complete one-shot Outlook dispatch."""
    cc_emails = cc_emails or []
    attachments = attachments or []

    # Format body into clean HTML if plaintext
    if "<p>" not in body and "<div>" not in body and "<br" not in body:
        paragraphs = body.split("\n\n")
        body_html = "".join(f"<p>{p.replace(chr(10), '<br>')}</p>" for p in paragraphs if p.strip())
        if not body_html:
            body_html = f"<p>{body}</p>"
    else:
        body_html = body

    # Privacy / Sensitive data check
    try:
        assert_payload_is_safe(subject, body_html)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Security Sanitizer Guard Triggered:{Colors.RESET} {e}")
        return False

    # Connect driver
    driver = WebBridgeDriver(daemon_url=daemon_url, session=session_name)
    if not check_webbridge_daemon(driver):
        return False

    provider = OutlookProvider(driver, OutlookSelectors())

    print(f"\n{Colors.BOLD}[1/6] Connecting to Outlook Mailbox...{Colors.RESET}")
    driver.navigate("https://outlook.live.com/mail/")
    time.sleep(1.0)

    print(f"{Colors.BOLD}[2/6] Opening compose pane...{Colors.RESET}")
    provider.open_compose(timeout_sec=20.0)
    time.sleep(0.6)
    print(f"      {Colors.GREEN}✓{Colors.RESET} Compose pane active")

    # Build recipients
    recipients = [Recipient(email=e, role=RecipientRole.TO) for e in to_emails]
    for cc in cc_emails:
        recipients.append(Recipient(email=cc, role=RecipientRole.CC))

    # Construct message
    msg = EmailMessage(
        subject=subject,
        body_html=body_html,
        recipients=recipients,
    )
    for a in attachments:
        msg.add_attachment(str(a))

    print(f"{Colors.BOLD}[3/6] Setting recipient pills (badge tokenization)...{Colors.RESET}")
    provider.set_recipients(msg.recipients)
    time.sleep(0.4)
    print(f"      {Colors.GREEN}✓{Colors.RESET} Recipients configured: {', '.join(to_emails)}")

    print(f"{Colors.BOLD}[4/6] Setting subject line...{Colors.RESET}")
    provider.set_subject(msg.subject)
    print(f"      {Colors.GREEN}✓{Colors.RESET} Subject: {msg.subject!r}")

    print(f"{Colors.BOLD}[5/6] Injecting message body...{Colors.RESET}")
    provider.set_body(msg.body_html)
    print(f"      {Colors.GREEN}✓{Colors.RESET} Body content injected")

    # Add attachments if any
    if attachments:
        print(f"{Colors.BOLD}[+] Uploading attachments...{Colors.RESET}")
        provider.add_attachments([str(a) for a in attachments])
        print(f"      {Colors.GREEN}✓{Colors.RESET} {len(attachments)} attachment(s) uploaded")

    time.sleep(0.5)

    # Optional visual verification screenshot
    if take_screenshot:
        screenshot_path = PROJECT_ROOT / "examples" / "compose_preview.png"
        try:
            shot = driver.take_screenshot(screenshot_path)
            print(f"      {Colors.DIM}📸 Screenshot saved to {shot}{Colors.RESET}")
        except Exception:
            pass

    # Pre-flight readiness audit
    readiness = provider.verify_readiness()
    print(f"\n{Colors.CYAN}{Colors.BOLD}── Pre-Flight Readiness Audit ──{Colors.RESET}")
    print(f"  • Pills Ready:   {readiness.get('pillsReady', False)} (valid: {readiness.get('validPillCount', 0)}, invalid: {readiness.get('invalidPillCount', 0)})")
    print(f"  • Subject Set:   {readiness.get('subjectSet', False)}")
    print(f"  • Body Set:      {readiness.get('bodySet', False)}")
    print(f"  • Overall Ready: {readiness.get('ready', False)}")

    if not readiness.get("subjectSet"):
        print(f"\n{Colors.RED}❌ Error: Subject was not detected in compose input. Aborting dispatch.{Colors.RESET}")
        return False

    if not readiness.get("bodySet"):
        print(f"\n{Colors.RED}❌ Error: Body was not detected. Aborting dispatch.{Colors.RESET}")
        return False

    if dry_run:
        print(f"\n{Colors.YELLOW}[DRY-RUN] Email prepared and verified. Skipping Send.{Colors.RESET}")
        return True

    # Dispatch
    print(f"\n{Colors.BOLD}[6/6] Dispatching email in one go...{Colors.RESET}")
    provider.send()
    print(f"      {Colors.GREEN}✓{Colors.RESET} Send signal fired (Ctrl+Enter / Send button)")

    # Post-send verification
    time.sleep(1.5)
    sent_confirmed = provider.verify_sent(timeout_sec=12.0)
    if sent_confirmed:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 SUCCESS! Email dispatched and compose pane closed cleanly.{Colors.RESET}")
    else:
        print(f"\n{Colors.YELLOW}⚠️  Compose pane still closing. Email has been handed to Outlook dispatch pipeline.{Colors.RESET}")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="One-shot autonomous Outlook Web email dispatcher.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-t", "--to", action="append", help="Recipient email address (can specify multiple)")
    parser.add_argument("-c", "--cc", action="append", default=[], help="Cc email address")
    parser.add_argument("-s", "--subject", help="Email subject line")
    parser.add_argument("-b", "--body", help="Email body (text or HTML)")
    parser.add_argument("--body-file", type=Path, help="Path to file containing email body")
    parser.add_argument("-a", "--attachment", action="append", default=[], help="File path to attach")
    parser.add_argument("-y", "--yes", action="store_true", help="Send immediately without asking for confirmation")
    parser.add_argument("--dry-run", action="store_true", help="Prepare and verify without clicking Send")
    parser.add_argument("--session", default="mail-cross-verify", help="WebBridge session name")
    parser.add_argument("--no-screenshot", action="store_true", help="Skip preview screenshot")

    args = parser.parse_args()

    print_banner()

    # Determine if CLI mode or Interactive mode
    has_cli_info = bool(args.to and args.subject and (args.body or args.body_file))

    if has_cli_info:
        to_emails = args.to
        cc_emails = args.cc
        subject = args.subject
        if args.body_file:
            if not args.body_file.is_file():
                print(f"{Colors.RED}Body file not found: {args.body_file}{Colors.RESET}")
                sys.exit(1)
            body = args.body_file.read_text(encoding="utf-8")
        else:
            body = args.body
        attachments = [Path(p) for p in args.attachment if Path(p).is_file()]
        skip_confirm = args.yes
    else:
        # Interactive mode
        data = get_interactive_inputs()
        to_emails = data["to"]
        cc_emails = data["cc"]
        subject = data["subject"]
        body = data["body"]
        attachments = data["attachments"]
        skip_confirm = args.yes

    # Summary box
    print(f"\n{Colors.CYAN}{Colors.BOLD}╔══════════════════════ DISPATCH SUMMARY ══════════════════════╗{Colors.RESET}")
    print(f"  {Colors.BOLD}To:{Colors.RESET}          {', '.join(to_emails)}")
    if cc_emails:
        print(f"  {Colors.BOLD}Cc:{Colors.RESET}          {', '.join(cc_emails)}")
    print(f"  {Colors.BOLD}Subject:{Colors.RESET}     {subject}")
    preview = body.replace("\n", " ")[:70] + ("..." if len(body) > 70 else "")
    print(f"  {Colors.BOLD}Body:{Colors.RESET}        {preview}")
    if attachments:
        print(f"  {Colors.BOLD}Attachments:{Colors.RESET} {', '.join(a.name for a in attachments)}")
    print(f"{Colors.CYAN}{Colors.BOLD}╚══════════════════════════════════════════════════════════════╝{Colors.RESET}\n")

    if not skip_confirm and not args.dry_run:
        choice = input(f"{Colors.BOLD}Ready to send now? [Y/n]: {Colors.RESET}").strip().lower()
        if choice not in ("", "y", "yes"):
            print(f"{Colors.YELLOW}Operation cancelled by user.{Colors.RESET}")
            sys.exit(0)

    success = send_mail(
        to_emails=to_emails,
        subject=subject,
        body=body,
        cc_emails=cc_emails,
        attachments=attachments,
        dry_run=args.dry_run,
        take_screenshot=not args.no_screenshot,
        session_name=args.session,
    )

    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
