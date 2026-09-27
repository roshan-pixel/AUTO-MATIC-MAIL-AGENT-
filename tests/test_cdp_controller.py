"""Tests for CDPController in auto_mail.drivers.cdp_controller."""

from auto_mail.drivers.cdp_controller import CDPController

def test_enter_key_payloads():
    down = CDPController.enter_key_down()
    assert down["method"] == "Input.dispatchKeyEvent"
    assert down["params"]["type"] == "keyDown"
    assert down["params"]["key"] == "Enter"
    assert down["params"]["windowsVirtualKeyCode"] == 13

    up = CDPController.enter_key_up()
    assert up["method"] == "Input.dispatchKeyEvent"
    assert up["params"]["type"] == "keyUp"
    assert up["params"]["key"] == "Enter"

def test_ctrl_enter_sequence():
    seq = CDPController.ctrl_enter()
    assert len(seq) == 4
    # 1. Control keyDown
    assert seq[0]["params"]["type"] == "keyDown"
    assert seq[0]["params"]["key"] == "Control"
    # 2. Enter keyDown with modifiers=2
    assert seq[1]["params"]["type"] == "keyDown"
    assert seq[1]["params"]["key"] == "Enter"
    assert seq[1]["params"]["modifiers"] == 2
    # 3. Enter keyUp
    assert seq[2]["params"]["type"] == "keyUp"
    assert seq[2]["params"]["key"] == "Enter"
    # 4. Control keyUp
    assert seq[3]["params"]["type"] == "keyUp"
    assert seq[3]["params"]["key"] == "Control"

def test_set_file_input_files():
    payload = CDPController.set_file_input_files(node_id=42, files=["/path/to/a.pdf"])
    assert payload["method"] == "DOM.setFileInputFiles"
    assert payload["params"]["nodeId"] == 42
    assert payload["params"]["files"] == ["/path/to/a.pdf"]
