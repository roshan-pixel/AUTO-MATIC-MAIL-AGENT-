"""Microsoft Outlook Web & Microsoft 365 Provider Engine.

Implements rock-solid recipient badge tokenization (resolving invalidPill red borders),
DOM contentEditable rich-text injection, and dispatch validation for outlook.live.com.
"""

import time
import json
from typing import List, Dict, Any, Optional
from .base_provider import BaseMailProvider
from ..models import Recipient, RecipientRole
from ..config import OutlookSelectors
from ..exceptions import ComposeTimeoutError, RecipientValidationError, ElementInteractionError

class OutlookProvider(BaseMailProvider):
    """Automation engine for Microsoft Outlook Web."""

    def __init__(self, driver, selectors: Optional[OutlookSelectors] = None):
        super().__init__(driver)
        self.selectors = selectors or OutlookSelectors()

    def open_mailbox(self) -> bool:
        """Navigates to Outlook Web inbox."""
        return self.driver.navigate("https://outlook.live.com/mail/")

    def open_compose(self, timeout_sec: float = 15.0) -> bool:
        """Opens the Outlook compose pane if not already active."""
        # Check if already open
        is_open_code = f"""(() => {{
            const toField = document.querySelector({json.dumps(self.selectors.to_field)});
            const subject = document.querySelector({json.dumps(self.selectors.subject_field)});
            return !!(toField && subject);
        }})()"""
        if self.driver.evaluate(is_open_code):
            return True

        # Click "New mail" or "New message" button
        click_code = f"""(() => {{
            const candidates = [
                {json.dumps(self.selectors.new_mail_button)},
                'button[aria-label*="New message"]',
                'button[title*="New message"]',
                'button[name="New message"]',
                'button[data-automation-id="newMessageButton"]',
                '[data-item-id="newMessage"]'
            ];
            for (const sel of candidates) {{
                try {{
                    const el = document.querySelector(sel);
                    if (el) {{ el.click(); return true; }}
                }} catch (e) {{}}
            }}
            const btn = Array.from(document.querySelectorAll('button, div[role="button"], span')).find(e => {{
                const txt = (e.innerText || '').trim().toLowerCase();
                return txt.startsWith('new mail') || txt.startsWith('new message') || txt === 'new';
            }});
            if (btn) {{
                btn.click();
                return true;
            }}
            return false;
        }})()"""
        clicked = self.driver.evaluate(click_code)
        if not clicked:
            raise ComposeTimeoutError("Could not find or click 'New mail' or 'New message' button in Outlook.")

        # Poll until compose fields appear
        start_time = time.time()
        while time.time() - start_time < timeout_sec:
            if self.driver.evaluate(is_open_code):
                time.sleep(0.3)
                return True
            time.sleep(0.5)

        raise ComposeTimeoutError("Outlook compose pane did not render within timeout.")

    def _insert_recipient_pill(self, field_selector: str, email: str) -> bool:
        """Inserts an email and commits it with CDP Enter to form a native validPill."""
        insert_code = f"""(() => {{
            let field = document.querySelector({json.dumps(field_selector)});
            if (!field) return false;
            const input = (field.tagName === 'INPUT' ? field : (field.querySelector('input, [contenteditable="true"]') || field));
            input.focus();
            if (input.tagName === 'INPUT') {{
                input.value = {json.dumps(email)};
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                input.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }} else {{
                document.execCommand('insertText', false, {json.dumps(email)});
            }}
            return true;
        }})()"""
        if not self.driver.evaluate(insert_code):
            return False

        time.sleep(0.1)
        # Dispatch native Enter via CDP
        self.driver.dispatch_enter()
        # Fallback event dispatch to ensure pill commits if CDP alone doesn't trigger UI listener
        commit_fallback = """(() => {
            const el = document.activeElement;
            if (el) {
                el.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }));
                el.dispatchEvent(new KeyboardEvent('keyup', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }));
            }
        })()"""
        self.driver.evaluate(commit_fallback)
        time.sleep(0.2)
        return True

    def set_recipients(self, recipients: List[Recipient]) -> bool:
        """Populates To, Cc, and Bcc fields with verified tokenized pills."""
        self.open_compose()

        for r in recipients:
            if r.role == RecipientRole.TO:
                target_selector = self.selectors.to_field
            elif r.role == RecipientRole.CC:
                # Ensure CC field is open
                ensure_cc = f"""(() => {{
                    let cc = document.querySelector({json.dumps(self.selectors.cc_field)});
                    if (!cc) {{
                        const btn = Array.from(document.querySelectorAll('button, span')).find(el => el.innerText === 'Cc' || (el.getAttribute('aria-label') && el.getAttribute('aria-label').includes('Cc')));
                        if (btn) btn.click();
                    }}
                    return true;
                }})()"""
                self.driver.evaluate(ensure_cc)
                time.sleep(0.2)
                target_selector = self.selectors.cc_field
            elif r.role == RecipientRole.BCC:
                # Ensure BCC field is open
                ensure_bcc = f"""(() => {{
                    let bcc = document.querySelector({json.dumps(self.selectors.bcc_field)});
                    if (!bcc) {{
                        const btn = Array.from(document.querySelectorAll('button, span')).find(el => el.innerText === 'Bcc' || (el.getAttribute('aria-label') && el.getAttribute('aria-label').includes('Bcc')));
                        if (btn) btn.click();
                    }}
                    return true;
                }})()"""
                self.driver.evaluate(ensure_bcc)
                time.sleep(0.2)
                target_selector = self.selectors.bcc_field

            success = self._insert_recipient_pill(target_selector, r.email)
            if not success:
                raise RecipientValidationError(r.email, f"Could not insert into {r.role.value} field")

        return True

    def set_subject(self, subject: str) -> bool:
        """Injects subject line and triggers event bubbling."""
        self.open_compose()
        code = f"""(() => {{
            const input = document.querySelector({json.dumps(self.selectors.subject_field)});
            if (!input) return false;
            input.focus();
            input.value = {json.dumps(subject)};
            input.dispatchEvent(new Event('input', {{ bubbles: true }}));
            input.dispatchEvent(new Event('change', {{ bubbles: true }}));
            return true;
        }})()"""
        res = self.driver.evaluate(code)
        if not res:
            raise ElementInteractionError("Failed to set subject line in Outlook compose.")
        return True

    def set_body(self, html_content: str) -> bool:
        """Injects rich HTML into Outlook's contentEditable editor."""
        self.open_compose()
        code = f"""(() => {{
            const editor = document.querySelector({json.dumps(self.selectors.body_field)});
            if (!editor) return false;
            editor.focus();
            editor.innerHTML = {json.dumps(html_content)};
            editor.dispatchEvent(new Event('input', {{ bubbles: true }}));
            return true;
        }})()"""
        res = self.driver.evaluate(code)
        if not res:
            raise ElementInteractionError("Failed to set body content in Outlook compose.")
        return True

    def add_attachments(self, file_paths: List[str]) -> bool:
        """Uploads one or more files to the Outlook email draft."""
        for path in file_paths:
            self.driver.upload_file(self.selectors.attachment_input, path)
            time.sleep(0.5)
        return True

    def verify_readiness(self) -> Dict[str, Any]:
        """Inspects recipient pills, subject, and editor state."""
        code = f"""(() => {{
            const invalidPills = Array.from(document.querySelectorAll({json.dumps(self.selectors.invalid_pill)})).map(p => p.innerText.trim());
            const validPills = Array.from(document.querySelectorAll({json.dumps(self.selectors.pill_container)})).filter(p => !p.className.includes('invalid')).map(p => p.innerText.trim());
            const subject = document.querySelector({json.dumps(self.selectors.subject_field)});
            const body = document.querySelector({json.dumps(self.selectors.body_field)});

            return {{
                ready: invalidPills.length === 0 && validPills.length > 0 && !!(subject && subject.value) && !!(body && body.innerText.trim().length > 0),
                pillsReady: invalidPills.length === 0 && validPills.length > 0,
                validPillCount: validPills.length,
                invalidPillCount: invalidPills.length,
                validPills: validPills,
                invalidPills: invalidPills,
                subjectSet: !!(subject && subject.value),
                bodySet: !!(body && body.innerText.trim().length > 0)
            }};
        }})()"""
        return self.driver.evaluate(code) or {}

    def send(self) -> bool:
        """Sends email using Send button or CDP Ctrl+Enter shortcut."""
        readiness = self.verify_readiness()
        if not readiness.get("ready"):
            raise ElementInteractionError(f"Cannot send email: readiness check failed {readiness}")

        # Dispatch Ctrl+Enter shortcut
        dispatched = self.driver.dispatch_key_combination("Enter", ["Control"])
        if dispatched:
            time.sleep(0.5)
            return True

        # Fallback: Click Send button
        click_code = f"""(() => {{
            const btn = document.querySelector({json.dumps(self.selectors.send_button)});
            if (btn) {{
                btn.click();
                return true;
            }}
            return false;
        }})()"""
        return bool(self.driver.evaluate(click_code))

    def verify_sent(self, timeout_sec: float = 10.0) -> bool:
        """Verifies compose pane closed and draft was dispatched."""
        start = time.time()
        is_compose_closed = f"""(() => {{
            const to = document.querySelector({json.dumps(self.selectors.to_field)});
            return !to;
        }})()"""
        while time.time() - start < timeout_sec:
            if self.driver.evaluate(is_compose_closed):
                return True
            time.sleep(0.5)
        return False
