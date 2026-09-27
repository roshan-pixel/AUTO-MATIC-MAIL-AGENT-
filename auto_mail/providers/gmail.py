"""Google Gmail Web Provider Engine.

Automates recipient chip tokenization, rich-text message body editing,
and verified delivery for mail.google.com.
"""

import time
import json
from typing import List, Dict, Any, Optional
from .base_provider import BaseMailProvider
from ..models import Recipient, RecipientRole
from ..config import GmailSelectors
from ..exceptions import ComposeTimeoutError, RecipientValidationError, ElementInteractionError

class GmailProvider(BaseMailProvider):
    """Automation engine for Google Gmail Web."""

    def __init__(self, driver, selectors: Optional[GmailSelectors] = None):
        super().__init__(driver)
        self.selectors = selectors or GmailSelectors()

    def open_mailbox(self) -> bool:
        """Navigates to Gmail inbox."""
        return self.driver.navigate("https://mail.google.com/mail/u/0/")

    def open_compose(self, timeout_sec: float = 15.0) -> bool:
        """Opens Gmail compose popup if not already present."""
        is_open_code = f"""(() => {{
            const subject = document.querySelector({json.dumps(self.selectors.subject_field)});
            const body = document.querySelector({json.dumps(self.selectors.body_field)});
            return !!(subject && body);
        }})()"""
        if self.driver.evaluate(is_open_code):
            return True

        # Click Compose button
        click_code = f"""(() => {{
            const candidates = [
                {json.dumps(self.selectors.compose_button)},
                'div[role="button"][gh="cm"]',
                'div[aria-label*="Compose"]',
                '.T-I.T-I-KE.L3'
            ];
            for (const sel of candidates) {{
                try {{
                    const el = document.querySelector(sel);
                    if (el) {{ el.click(); return true; }}
                }} catch (e) {{}}
            }}
            const btn = Array.from(document.querySelectorAll('div[role=\"button\"], button')).find(el => {{
                const txt = (el.innerText || '').trim().toLowerCase();
                return txt === 'compose' || txt.includes('compose');
            }});
            if (btn) {{
                btn.click();
                return true;
            }}
            return false;
        }})()"""
        clicked = self.driver.evaluate(click_code)
        if not clicked:
            raise ComposeTimeoutError("Could not find or click 'Compose' button in Gmail.")

        # Wait for compose window to open
        start_time = time.time()
        while time.time() - start_time < timeout_sec:
            if self.driver.evaluate(is_open_code):
                time.sleep(0.3)
                return True
            time.sleep(0.5)

        raise ComposeTimeoutError("Gmail compose dialog did not open within timeout.")

    def _insert_recipient_chip(self, field_selector: str, email: str) -> bool:
        """Inserts email address and presses Enter to chip it."""
        insert_code = f"""(() => {{
            let field = document.querySelector({json.dumps(field_selector)});
            if (!field) return false;
            const input = (field.tagName === 'INPUT' ? field : (field.querySelector('input') || field));
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
        self.driver.dispatch_enter()
        # Fallback keydown event
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
        """Populates To, Cc, and Bcc in Gmail."""
        self.open_compose()

        for r in recipients:
            if r.role == RecipientRole.TO:
                target_selector = self.selectors.to_field
            elif r.role == RecipientRole.CC:
                # Click 'Add Cc' link if needed
                ensure_cc = f"""(() => {{
                    let cc = document.querySelector({json.dumps(self.selectors.cc_field)});
                    if (!cc) {{
                        const btn = document.querySelector({json.dumps(self.selectors.cc_button)});
                        if (btn) btn.click();
                    }}
                    return true;
                }})()"""
                self.driver.evaluate(ensure_cc)
                time.sleep(0.2)
                target_selector = self.selectors.cc_field
            elif r.role == RecipientRole.BCC:
                # Click 'Add Bcc' link if needed
                ensure_bcc = f"""(() => {{
                    let bcc = document.querySelector({json.dumps(self.selectors.bcc_field)});
                    if (!bcc) {{
                        const btn = document.querySelector({json.dumps(self.selectors.bcc_button)});
                        if (btn) btn.click();
                    }}
                    return true;
                }})()"""
                self.driver.evaluate(ensure_bcc)
                time.sleep(0.2)
                target_selector = self.selectors.bcc_field

            success = self._insert_recipient_chip(target_selector, r.email)
            if not success:
                raise RecipientValidationError(r.email, f"Could not insert into Gmail {r.role.value} field")

        return True

    def set_subject(self, subject: str) -> bool:
        """Sets subject line in Gmail compose using native fill (primary) then JS fallback."""
        self.open_compose()
        # Wait for compose to fully render
        time.sleep(0.5)

        # Primary: WebBridge native fill — most reliable for <input> elements
        if hasattr(self.driver, "fill"):
            try:
                result = self.driver.fill(self.selectors.subject_field, subject)
                if result:
                    time.sleep(0.2)
                    return True
            except Exception:
                pass

        # Fallback: Native property setter to bypass React controlled-input
        code = f"""(() => {{
            const input = document.querySelector({json.dumps(self.selectors.subject_field)});
            if (!input) return false;
            input.focus();
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            nativeInputValueSetter.call(input, {json.dumps(subject)});
            input.dispatchEvent(new Event('input', {{ bubbles: true }}));
            input.dispatchEvent(new Event('change', {{ bubbles: true }}));
            input.dispatchEvent(new KeyboardEvent('keyup', {{ bubbles: true }}));
            return input.value === {json.dumps(subject)};
        }})()"""
        res = self.driver.evaluate(code)
        if not res:
            raise ElementInteractionError("Failed to set subject line in Gmail compose.")
        time.sleep(0.2)
        return True


    def set_body(self, html_content: str) -> bool:
        """Injects rich HTML into Gmail message body with TrustedHTML compatibility."""
        self.open_compose()
        # Prefer native driver fill if available (handles contenteditable cleanly)
        if hasattr(self.driver, "fill"):
            try:
                import re
                plain = re.sub(r'</?(?:p|div|h\d|tr)>', '\n', html_content)
                plain = re.sub(r'<br\s*/?>', '\n', plain)
                plain = re.sub(r'<[^>]+>', '', plain).strip()
                if self.driver.fill(self.selectors.body_field, plain or html_content):
                    return True
            except Exception:
                pass

        # Trusted Types / DOM injection fallback
        code = f"""(() => {{
            const editor = document.querySelector({json.dumps(self.selectors.body_field)});
            if (!editor) return false;
            editor.focus();
            try {{
                if (window.trustedTypes) {{
                    let policy = window.trustedTypes.defaultPolicy;
                    if (!policy) {{
                        try {{ policy = window.trustedTypes.createPolicy('gmail-body-policy', {{ createHTML: s => s }}); }} catch (e) {{}}
                    }}
                    if (policy) {{
                        editor.innerHTML = policy.createHTML({json.dumps(html_content)});
                        editor.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        return true;
                    }}
                }}
            }} catch (e) {{}}
            try {{
                editor.innerHTML = {json.dumps(html_content)};
                editor.dispatchEvent(new Event('input', {{ bubbles: true }}));
                return true;
            }} catch (e) {{
                editor.innerText = {json.dumps(html_content)};
                editor.dispatchEvent(new Event('input', {{ bubbles: true }}));
                return true;
            }}
        }})()"""
        res = self.driver.evaluate(code)
        if not res:
            raise ElementInteractionError("Failed to set body content in Gmail compose.")
        return True

    def add_attachments(self, file_paths: List[str]) -> bool:
        """Uploads files to Gmail draft."""
        for path in file_paths:
            self.driver.upload_file(self.selectors.attachment_input, path)
            time.sleep(0.5)
        return True

    def verify_readiness(self) -> Dict[str, Any]:
        """Inspects Gmail compose state prior to sending."""
        code = f"""(() => {{
            const subject = document.querySelector({json.dumps(self.selectors.subject_field)});
            const body = document.querySelector({json.dumps(self.selectors.body_field)});
            const chips = Array.from(document.querySelectorAll({json.dumps(self.selectors.chip_container)})).map(el => el.innerText.trim()).filter(Boolean);

            return {{
                ready: chips.length > 0 && !!(subject && subject.value) && !!(body && body.innerText.trim().length > 0),
                chipsReady: chips.length > 0,
                recipientChipCount: chips.length,
                chips: chips,
                subjectSet: !!(subject && subject.value),
                bodySet: !!(body && body.innerText.trim().length > 0)
            }};
        }})()"""
        return self.driver.evaluate(code) or {}

    def send(self) -> bool:
        """Sends email in Gmail via Ctrl+Enter or Send button."""
        readiness = self.verify_readiness()
        if not readiness.get("ready"):
            raise ElementInteractionError(f"Cannot send email: readiness check failed {readiness}")

        # Send via Ctrl+Enter
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
        """Verifies 'Message sent' toast or compose dialog close."""
        start = time.time()
        is_sent_code = """(() => {
            const toast = Array.from(document.querySelectorAll('div[role="alert"], span.b8')).find(el => el.innerText && el.innerText.includes('Message sent'));
            const compose = document.querySelector('div[role="dialog"]');
            return !!toast || !compose;
        })()"""
        while time.time() - start < timeout_sec:
            if self.driver.evaluate(is_sent_code):
                return True
            time.sleep(0.5)
        return False
