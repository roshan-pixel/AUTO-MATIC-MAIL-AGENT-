"""Tests for data models in auto_mail.models."""

import pytest
from pathlib import Path
from auto_mail.models import EmailMessage, Recipient, RecipientRole, Attachment, ProviderType

def test_recipient_valid():
    r = Recipient(email="Test.User@example.com", name="Test User", role=RecipientRole.TO)
    assert r.email == "test.user@example.com"
    assert r.role == RecipientRole.TO
    assert r.name == "Test User"

def test_recipient_invalid_email():
    with pytest.raises(ValueError):
        Recipient(email="invalid-email-address")

def test_email_message_builder(tmp_path):
    dummy_file = tmp_path / "document.pdf"
    dummy_file.write_text("dummy content")

    msg = EmailMessage(
        subject="Important Notice",
        body_html="<p>Notice details</p>"
    )
    msg.add_to("to1@example.com")
    msg.add_to("to2@example.com")
    msg.add_cc("cc1@example.com")
    msg.add_bcc("bcc1@example.com")
    msg.add_attachment(str(dummy_file))

    assert len(msg.recipients) == 4
    assert len(msg.to_recipients) == 2
    assert len(msg.cc_recipients) == 1
    assert len(msg.bcc_recipients) == 1
    assert len(msg.attachments) == 1
    assert msg.attachments[0].path == dummy_file.resolve()

def test_attachment_nonexistent_file():
    with pytest.raises(ValueError):
        Attachment(path=Path("non_existent_file_xyz_12345.pdf"))
