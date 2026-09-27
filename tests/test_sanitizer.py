"""Tests for security sanitizer in auto_mail.security.sanitizer."""

import pytest
from auto_mail.security.sanitizer import (
    DataSanitizer,
    assert_payload_is_safe,
    is_luhn_valid,
    redact_sensitive_data
)
from auto_mail.exceptions import DataSanitizationError

def test_luhn_validation():
    # 4532015112830366 is a standard 16-digit valid Luhn test card number
    assert is_luhn_valid("4532015112830366") is True
    assert is_luhn_valid("4532015112830367") is False
    assert is_luhn_valid("123") is False

def test_sanitizer_safe_payload():
    safe_subject = "Formal Grievance: Billing issue on invoice INV-2026-001"
    safe_body = "<p>My registered account is roshan@example.com. Paid $1.00 via DCB Bank.</p>"
    # Should not raise
    assert_payload_is_safe(safe_subject, safe_body)

def test_sanitizer_cvv_leak():
    subject = "Support Query"
    body = "Here is my card with cvv: 789 and valid thru 12/28"
    with pytest.raises(DataSanitizationError) as exc_info:
        assert_payload_is_safe(subject, body)
    assert "CVV/CVC Security Code" in str(exc_info.value)

def test_sanitizer_private_key_leak():
    subject = "Server error"
    body = "-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA0...\n-----END RSA PRIVATE KEY-----"
    with pytest.raises(DataSanitizationError) as exc_info:
        assert_payload_is_safe(subject, body)
    assert "Cryptographic Private Key Block" in str(exc_info.value)

def test_redact_sensitive_data():
    raw = "My security code: 456"
    cleaned = redact_sensitive_data(raw)
    assert "456" not in cleaned
    assert "[REDACTED_CVV]" in cleaned
