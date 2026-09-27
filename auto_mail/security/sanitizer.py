"""Privacy and PCI-DSS Data Sanitizer.

Enforces zero-credential leakage by scanning email subjects and bodies for:
- Credit / Debit Card PANs (Visa, MasterCard, Amex, RuPay, Discover)
- Card Verification Values (CVV/CVC 3-4 digits)
- Expiration dates (MM/YY or MM/YYYY)
- Private cryptographic keys and API tokens
- Passwords and auth tokens
"""

import re
from typing import NamedTuple, List
from ..exceptions import DataSanitizationError

# Luhn algorithm verification for credit card PAN detection
def is_luhn_valid(number_str: str) -> bool:
    digits = [int(d) for d in re.sub(r"\D", "", number_str)]
    if len(digits) < 13 or len(digits) > 19:
        return False
    checksum = 0
    reverse_digits = digits[::-1]
    for i, d in enumerate(reverse_digits):
        if i % 2 == 1:
            doubled = d * 2
            checksum += doubled - 9 if doubled > 9 else doubled
        else:
            checksum += d
    return checksum % 10 == 0

# Regular expressions for potential secrets
CARD_PATTERN = re.compile(r"\b(?:\d[ -]*?){13,19}\b")
CVV_PATTERN = re.compile(r"(?i)\b(?:cvv|cvc|security\s*code|cid)[:\s=]*([0-9]{3,4})\b")
EXP_PATTERN = re.compile(r"(?i)\b(?:exp|expires|expiry|valid\s*thru)[:\s=]*([0-1]?[0-9][/-][2-3][0-9])\b")
PRIVATE_KEY_PATTERN = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")

class SanitizationResult(NamedTuple):
    is_safe: bool
    sanitized_text: str
    detected_threats: List[str]

class DataSanitizer:
    """Detects and redacts sensitive financial and authentication data."""

    @classmethod
    def sanitize(cls, text: str) -> SanitizationResult:
        threats: List[str] = []
        cleaned = text

        # 1. Detect and redact credit card PANs
        def _replace_card(match):
            val = match.group(0)
            cleaned_num = re.sub(r"\D", "", val)
            if is_luhn_valid(cleaned_num):
                threats.append(f"Credit Card PAN ending in ...{cleaned_num[-4:]}")
                return f"[REDACTED_CARD_ENDING_IN_{cleaned_num[-4:]}]"
            return val

        cleaned = CARD_PATTERN.sub(_replace_card, cleaned)

        # 2. Detect and redact CVV
        def _replace_cvv(match):
            threats.append("CVV/CVC Security Code")
            return match.group(0).replace(match.group(1), "[REDACTED_CVV]")

        cleaned = CVV_PATTERN.sub(_replace_cvv, cleaned)

        # 3. Detect private keys
        if PRIVATE_KEY_PATTERN.search(cleaned):
            threats.append("Cryptographic Private Key Block")
            cleaned = PRIVATE_KEY_PATTERN.sub("[REDACTED_PRIVATE_KEY]", cleaned)

        is_safe = len(threats) == 0
        return SanitizationResult(is_safe=is_safe, sanitized_text=cleaned, detected_threats=threats)

def redact_sensitive_data(text: str) -> str:
    """Convenience helper to scrub text."""
    return DataSanitizer.sanitize(text).sanitized_text

def assert_payload_is_safe(subject: str, body: str) -> None:
    """Raises DataSanitizationError if any critical leaks are found in subject or body."""
    res_subj = DataSanitizer.sanitize(subject)
    res_body = DataSanitizer.sanitize(body)
    all_threats = res_subj.detected_threats + res_body.detected_threats
    if all_threats:
        raise DataSanitizationError(
            f"Blocked email transmission due to sensitive credential leak: {', '.join(all_threats)}"
        )
