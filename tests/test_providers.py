"""Tests for Outlook and Gmail provider orchestration with MockDriver."""

import pytest
from unittest.mock import MagicMock
from auto_mail.providers.outlook import OutlookProvider
from auto_mail.providers.gmail import GmailProvider
from auto_mail.models import Recipient, RecipientRole
from auto_mail.config import OutlookSelectors, GmailSelectors

class MockDriver:
    def __init__(self):
        self.evaluated_scripts = []
        self.dispatched_keys = []
        self.eval_return_value = True

    def navigate(self, url: str) -> bool:
        return True

    def evaluate(self, js_code: str):
        self.evaluated_scripts.append(js_code)
        if isinstance(self.eval_return_value, dict):
            return self.eval_return_value
        return self.eval_return_value

    def dispatch_enter(self) -> bool:
        self.dispatched_keys.append("Enter")
        return True

    def dispatch_key_combination(self, key: str, modifiers: list) -> bool:
        self.dispatched_keys.append(f"{'+'.join(modifiers)}+{key}")
        return True

    def upload_file(self, selector: str, path: str) -> bool:
        return True

def test_outlook_provider_recipient_setting():
    driver = MockDriver()
    provider = OutlookProvider(driver)

    recipients = [
        Recipient(email="to@example.com", role=RecipientRole.TO),
        Recipient(email="cc@example.com", role=RecipientRole.CC),
        Recipient(email="bcc@example.com", role=RecipientRole.BCC)
    ]

    res = provider.set_recipients(recipients)
    assert res is True
    # Verify native Enter was dispatched for each recipient pill
    assert driver.dispatched_keys.count("Enter") == 3

def test_gmail_provider_recipient_setting():
    driver = MockDriver()
    provider = GmailProvider(driver)

    recipients = [
        Recipient(email="to@example.com", role=RecipientRole.TO),
        Recipient(email="cc@example.com", role=RecipientRole.CC)
    ]

    res = provider.set_recipients(recipients)
    assert res is True
    assert driver.dispatched_keys.count("Enter") == 2

def test_outlook_readiness_verification():
    driver = MockDriver()
    provider = OutlookProvider(driver)

    driver.eval_return_value = {
        "ready": True,
        "pillsReady": True,
        "validPillCount": 2,
        "invalidPillCount": 0,
        "validPills": ["to@example.com", "cc@example.com"],
        "invalidPills": [],
        "subjectSet": True,
        "bodySet": True
    }

    readiness = provider.verify_readiness()
    assert readiness["ready"] is True
    assert readiness["validPillCount"] == 2
    assert readiness["invalidPillCount"] == 0

def test_gmail_readiness_verification():
    driver = MockDriver()
    provider = GmailProvider(driver)

    driver.eval_return_value = {
        "ready": True,
        "chipsReady": True,
        "recipientChipCount": 2,
        "chips": ["to@example.com", "cc@example.com"],
        "subjectSet": True,
        "bodySet": True
    }

    readiness = provider.verify_readiness()
    assert readiness["ready"] is True
    assert readiness["recipientChipCount"] == 2
