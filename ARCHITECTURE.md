# AUTO-MATIC-MAIL-AGENT: System Architecture & Technical Specifications 🏛️

> **Comprehensive Engineering Blueprint, Flow Diagrams, Security Protocols & Codebase Navigation**  
> *Target Environments: Microsoft 365 / Outlook Live Web, Google Gmail Web, RFC 5321 SMTP*

---

## 📑 Document Structure
1. [System Architecture Diagram](#1-system-architecture-diagram)
2. [Core Engineering Highlights](#2-core-engineering-highlights)
3. [End-to-End Sequence Flow](#3-end-to-end-sequence-flow)
4. [Graphify Knowledge Graph & Codebase Navigation](#4-graphify-knowledge-graph--codebase-navigation)
5. [Complete Python Source File Index & Specifications](#5-complete-python-source-file-index--specifications)
6. [One-Shot Outlook Mail Dispatcher (`send_outlook.py`)](#6-one-shot-outlook-mail-dispatcher-send_outlookpy)
7. [Provider Automation & DOM Engineering](#7-provider-automation--dom-engineering)
8. [Data Privacy & PCI-DSS Sanitizer Layer](#8-data-privacy--pci-dss-sanitizer-layer)
9. [Driver & Protocol Abstraction Layer](#9-driver--protocol-abstraction-layer)

---

## 1. System Architecture Diagram

```mermaid
flowchart TD
    subgraph ClientLayer ["Client & Interface Layer"]
        CLI["One-Shot CLI (send_outlook.py)"]
        AgentCLI["Master CLI (python -m auto_mail.agent)"]
        Diagnostics["Diagnostic Suites (test_cdp_pills.py)"]
        Legal["Statutory Templates (auto_mail/templates/)"]
    end

    subgraph CoreEngine ["Core Orchestration & Security"]
        Agent["MailAgent Orchestrator (auto_mail/agent.py)"]
        Sanitizer["DataSanitizer & Luhn Guard (auto_mail/security/sanitizer.py)"]
        Config["AgentConfig & DOM Selectors (auto_mail/config.py)"]
        Models["Pydantic Data Models (auto_mail/models.py)"]
        Exceptions["Exception Hierarchy (auto_mail/exceptions.py)"]
    end

    subgraph ProvidersLayer ["Provider Automation Engines"]
        Outlook["OutlookProvider (auto_mail/providers/outlook.py)"]
        Gmail["GmailProvider (auto_mail/providers/gmail.py)"]
        BaseProvider["BaseMailProvider (auto_mail/providers/base_provider.py)"]
    end

    subgraph DriversLayer ["Driver & Protocol Abstraction"]
        WebBridge["WebBridgeDriver (auto_mail/drivers/webbridge.py)"]
        CDP["CDPController (auto_mail/drivers/cdp_controller.py)"]
        Playwright["PlaywrightDriver (auto_mail/drivers/playwright_driver.py)"]
        SMTP["SMTPDriver (auto_mail/drivers/smtp_driver.py)"]
    end

    subgraph ExecutionTargets ["Execution Targets & Runtime"]
        ActiveBrowser["Active User Browser Session (Port 10086 / WebBridge)"]
        HeadlessBrowser["Headless Chromium Context (Playwright)"]
        MailServer["Direct Mail Transfer Agent (MTA / smtplib)"]
    end

    CLI --> Outlook
    CLI --> WebBridge
    AgentCLI --> Agent
    Diagnostics --> Outlook
    Diagnostics --> Gmail
    Legal --> Agent

    Agent --> Models
    Agent --> Sanitizer
    Agent --> Config
    Agent --> Outlook
    Agent --> Gmail

    Outlook -- inherits --> BaseProvider
    Gmail -- inherits --> BaseProvider

    BaseProvider --> WebBridge
    BaseProvider --> Playwright
    BaseProvider --> SMTP

    WebBridge --> CDP
    WebBridge --> ActiveBrowser
    Playwright --> HeadlessBrowser
    SMTP --> MailServer
```

---

## 2. Core Engineering Highlights

### I. Chrome DevTools Protocol (CDP) Virtual Keycode Tokenization
* **Root Problem**: Injecting email addresses into modern Single Page Application (SPA) webmail clients (like Microsoft Outlook's Fluent UI or Google Gmail) via standard DOM `.value` setter fails to trigger internal React/Angular state transitions. In Outlook, uncommitted text generates red-bordered `invalidPill` spans that actively disable the Send action.
* **Architecture**: Combines `document.execCommand('insertText')` with raw Chrome DevTools Protocol `Input.dispatchKeyEvent` events using Windows Virtual KeyCode `13` (`Enter`).
* **Pre-Flight Inspection**: Inspects the live DOM for `[class*="personaPill"]`, `[class*="validPill"]`, and verifies that `[class*="invalidPill"]` count is strictly zero.

### II. Resilient Subject & ContentEditable Injection (TrustedHTML & React Setters)
* **Outlook Web**: Uses a dual-path mechanism:
  1. Primary: Native WebBridge `/command` `fill` tool which bypasses DOM synthetic events.
  2. Fallback: JavaScript native property descriptor getter/setter (`Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set`) combined with simulated `input`, `change`, and `keyup` bubbling.
* **Gmail Trusted Types**: Overcomes Gmail's strict `TrustedHTML` Content Security Policy (CSP). Standard `innerHTML` assignments throw `TypeError: This document requires 'TrustedHTML' assignment`. The engine dynamically detects `window.trustedTypes`, acquires or instantiates a policy, or delegates to native WebBridge `fill`.

### III. Zero-Leakage Privacy & PCI-DSS Data Sanitizer
* **Luhn Algorithm Checksum**: Mathematically analyzes all 13-19 digit number sequences (`is_luhn_valid`) to detect genuine credit/debit card Primary Account Numbers (Visa, MasterCard, Amex, RuPay, Discover), while preventing false positives on 16-character alphanumeric tracking codes.
* **Secret Redaction**: Regex-based scanners scrub 3-4 digit CVV/CVC codes, expiration dates, and OpenSSH / RSA PEM cryptographic private key headers before any network packet or browser automation keystroke is generated.

### IV. Session Borrowing & Zero-Auth Friction
* **Daemon Protocol**: Communicates with the user's authentic browser context via the Kimi WebBridge daemon (`127.0.0.1:10086`).
* **Tab Borrowing**: Automatically locates and re-uses existing Outlook/Gmail tabs, preserving 2FA logins, cookies, and corporate SSO states without credential storage.

---

## 3. End-to-End Sequence Flow

```mermaid
sequenceDiagram
    autonumber
    actor User as User / Script
    participant Runner as send_outlook.py / MailAgent
    participant Sanitizer as Security Sanitizer
    participant Provider as OutlookProvider / GmailProvider
    participant Driver as WebBridgeDriver (CDP)
    participant DOM as Webmail DOM (Outlook/Gmail)

    User->>Runner: Execute dispatch (To, Subject, Body, Attachments)
    
    rect rgb(240, 245, 255)
        note right of Runner: Phase 1: Security Audit
        Runner->>Sanitizer: assert_payload_is_safe(subject, body_html)
        Sanitizer->>Sanitizer: Run Luhn card check, CVV regex, Key scanner
        Sanitizer-->>Runner: Verified Safe (No sensitive data leaks)
    end

    rect rgb(245, 255, 245)
        note right of Runner: Phase 2: Tab Acquisition & Compose
        Runner->>Provider: open_mailbox()
        Provider->>Driver: navigate("https://outlook.live.com/mail/")
        Driver->>DOM: Find or borrow active tab
        Runner->>Provider: open_compose()
        Provider->>DOM: Locate & click "New mail" button
        DOM-->>Provider: Compose pane rendered & ready
    end

    rect rgb(255, 250, 240)
        note right of Runner: Phase 3: Recipient Tokenization
        Runner->>Provider: set_recipients(recipients)
        loop For each recipient
            Provider->>DOM: Focus input & insert email string
            Provider->>Driver: dispatch_enter() [CDP Input.dispatchKeyEvent]
            Driver->>DOM: Commit Enter keycode 13
            Provider->>DOM: Verify valid badge created
        end
    end

    rect rgb(255, 245, 245)
        note right of Runner: Phase 4: Subject, Body & Attachments
        Runner->>Provider: set_subject(subject)
        Provider->>DOM: Fill subject field (Native fill + Event bubbling)
        Runner->>Provider: set_body(body_html)
        Provider->>DOM: Inject rich text into editor
        opt Has Attachments
            Runner->>Provider: add_attachments(file_paths)
            Provider->>Driver: upload_file(attachment_input, path)
        end
    end

    rect rgb(245, 240, 255)
        note right of Runner: Phase 5: Verification & Dispatch
        Runner->>Provider: verify_readiness()
        Provider->>DOM: Query pillsReady, subjectSet, bodySet
        DOM-->>Provider: Readiness metrics (ready: true)
        Runner->>Provider: send()
        Provider->>Driver: dispatch_key_combination("Enter", ["Control"])
        Driver->>DOM: Fire Ctrl+Enter shortcut (Fallback: Click Send)
        Provider->>DOM: verify_sent() [Wait for compose pane to close]
        DOM-->>Provider: Compose closed (Confirmed Sent)
    end

    Runner-->>User: Delivery Success Report (Timing, Badges, Metrics)
```

---

## 4. Graphify Knowledge Graph & Codebase Navigation

The architecture, dependencies, and call graphs are indexed in the **Graphify Knowledge Graph** at `graphify-out/`.

### Knowledge Graph Metrics
* **Total Entities (Nodes)**: `343`
* **Total Relationships (Edges)**: `486`
* **Clustered Communities**: `36`
* **Graph Manifest**: Stored in `graphify-out/graph.json` and visualizable via `graphify-out/graph.html`.

### Key Architectural Hubs ("God Nodes")
1. **`OutlookProvider`** (`auto_mail/providers/outlook.py`) — Central engine for Microsoft 365 / Outlook Live DOM handling, recipient badge tokenization, and subject/body injection.
2. **`GmailProvider`** (`auto_mail/providers/gmail.py`) — Central engine for Google Gmail DOM handling, chip badges, and TrustedHTML policy compatibility.
3. **`WebBridgeDriver`** (`auto_mail/drivers/webbridge.py`) — Communication bus bridging local Python execution with Chrome/Edge via WebSocket and HTTP `/command` socket.
4. **`CDPController`** (`auto_mail/drivers/cdp_controller.py`) — Chrome DevTools Protocol key payload serializer for virtual keystrokes and file uploads.
5. **`MailAgent`** (`auto_mail/agent.py`) — Master facade orchestrator coordinating security audits, drivers, and providers.
6. **`EmailMessage`** (`auto_mail/models.py`) — Pydantic domain model enforcing valid recipient formatting and email structures.

---

## 5. Complete Python Source File Index & Specifications

Every `.py` file in the project has a strict architectural responsibility:

| File Path | Module Role | Key Classes / Functions | Primary Responsibility |
|---|---|---|---|
| [`send_outlook.py`](send_outlook.py) | **One-Shot Dispatcher** | `send_mail()`, `get_interactive_inputs()`, `main()` | Single-command or interactive zero-touch Outlook mail sending. |
| [`auto_mail/__init__.py`](auto_mail/__init__.py) | Package Root | `MailAgent`, `EmailMessage`, `Recipient`, `ProviderType` | Public interface exports. |
| [`auto_mail/agent.py`](auto_mail/agent.py) | Master Orchestrator | `MailAgent`, `main()` | High-level orchestration, multi-provider routing, CLI entrypoint. |
| [`auto_mail/config.py`](auto_mail/config.py) | Configuration Layer | `AgentConfig`, `OutlookSelectors`, `GmailSelectors`, `WebBridgeConfig` | Selectors and environment defaults. |
| [`auto_mail/exceptions.py`](auto_mail/exceptions.py) | Error Hierarchy | `MailAgentError`, `ComposeTimeoutError`, `RecipientValidationError` | Domain exception definitions. |
| [`auto_mail/models.py`](auto_mail/models.py) | Data Layer | `EmailMessage`, `Recipient`, `Attachment`, `RecipientRole` | Pydantic validation and email structure. |
| [`auto_mail/drivers/__init__.py`](auto_mail/drivers/__init__.py) | Driver Root | Re-exports all driver classes | Driver package entrypoint. |
| [`auto_mail/drivers/base.py`](auto_mail/drivers/base.py) | Driver Contract | `BaseMailDriver` | Abstract protocol methods. |
| [`auto_mail/drivers/cdp_controller.py`](auto_mail/drivers/cdp_controller.py) | CDP Engine | `CDPController` | Keycodes, key combinations, and CDP payloads. |
| [`auto_mail/drivers/webbridge.py`](auto_mail/drivers/webbridge.py) | WebBridge Driver | `WebBridgeDriver` | HTTP client for daemon `:10086`, `fill()`, `evaluate()`. |
| [`auto_mail/drivers/playwright_driver.py`](auto_mail/drivers/playwright_driver.py) | Playwright Driver | `PlaywrightDriver` | Headless Chromium automation for CI/CD. |
| [`auto_mail/drivers/smtp_driver.py`](auto_mail/drivers/smtp_driver.py) | Protocol Driver | `SMTPDriver` | RFC 5321 direct MTA delivery fallback. |
| [`auto_mail/providers/__init__.py`](auto_mail/providers/__init__.py) | Provider Root | Re-exports provider engines | Provider package entrypoint. |
| [`auto_mail/providers/base_provider.py`](auto_mail/providers/base_provider.py) | Provider Contract | `BaseMailProvider` | Abstract provider interface. |
| [`auto_mail/providers/outlook.py`](auto_mail/providers/outlook.py) | Outlook Engine | `OutlookProvider` | Outlook DOM automation, badge pills, subject/body fill. |
| [`auto_mail/providers/gmail.py`](auto_mail/providers/gmail.py) | Gmail Engine | `GmailProvider` | Gmail DOM automation, recipient chips, TrustedHTML. |
| [`auto_mail/security/__init__.py`](auto_mail/security/__init__.py) | Security Root | Re-exports security components | Security package entrypoint. |
| [`auto_mail/security/sanitizer.py`](auto_mail/security/sanitizer.py) | PCI & Privacy Guard | `assert_payload_is_safe()`, `is_luhn_valid()`, `redact_sensitive_data()` | Credit card PAN, CVV, and private key detection. |
| [`auto_mail/templates/__init__.py`](auto_mail/templates/__init__.py) | Templates Root | Re-exports template generators | Template package entrypoint. |
| [`auto_mail/templates/legal_grievance.py`](auto_mail/templates/legal_grievance.py) | Legal Generator | `generate_grievance_email()` | Statutory notice generator (India & Singapore). |
| [`auto_mail/templates/student_pack_claim.py`](auto_mail/templates/student_pack_claim.py) | Developer Generator | `generate_claim_email()` | GitHub Student Pack claim letter generator. |
| [`examples/send_outlook_only.py`](examples/send_outlook_only.py) | Focused Runner | Standalone script | Verified Outlook-only dispatch with screenshot audit. |
| [`examples/run_cross_verification.py`](examples/run_cross_verification.py) | Cross-Verification | Standalone script | Bi-directional Outlook ↔ Gmail cross-send test. |
| [`examples/test_cdp_pills.py`](examples/test_cdp_pills.py) | Diagnostic CLI | Diagnostic script | Tokenizes pills and chips without sending. |
| [`examples/send_outlook_grievance.py`](examples/send_outlook_grievance.py) | Example | Standalone script | Dispatches statutory legal notice via Outlook. |
| [`examples/send_gmail_notice.py`](examples/send_gmail_notice.py) | Example | Standalone script | Dispatches cloud deployment notice via Gmail. |
| [`examples/multi_provider_sync.py`](examples/multi_provider_sync.py) | Example | Standalone script | Demonstrates multi-provider orchestration. |
| [`tests/test_cdp_controller.py`](tests/test_cdp_controller.py) | Unit Tests | `pytest` test functions | Tests CDP payload generation and keycodes. |
| [`tests/test_models.py`](tests/test_models.py) | Unit Tests | `pytest` test functions | Tests Pydantic validation, email syntax, attachments. |
| [`tests/test_providers.py`](tests/test_providers.py) | Unit Tests | `pytest` test functions | Tests Outlook and Gmail provider logic with `MockDriver`. |
| [`tests/test_sanitizer.py`](tests/test_sanitizer.py) | Unit Tests | `pytest` test functions | Tests Luhn checksum, CVV detector, key leak guard. |

---

## 6. One-Shot Outlook Mail Dispatcher (`send_outlook.py`)

The root `send_outlook.py` script provides the fastest, most reliable way to send an email via Outlook Web.

### Execution Modes

#### 1. Interactive Mode
```bash
python send_outlook.py
```
* Asks for recipient `To: ` (validates syntax).
* Optional `Cc: `.
* Prompts for `Subject: `.
* Body entry: single-line, `MULTI` for multi-line block, or `@path/to/file.html` to load from disk.
* Optional attachment file path.
* Displays a formatted terminal preview table.
* On confirmation (`[Y/n]`), completes the dispatch in one go.

#### 2. Direct CLI Command
```bash
# Direct dispatch with automatic confirmation
python send_outlook.py -t sgarmy200@gmail.com -s "Project Milestone" -b "Milestone completed." -y

# With CC, attachment, and external HTML body file
python send_outlook.py \
  -t "sgarmy200@gmail.com" \
  -c "lead@company.com" \
  -s "Sprint Review" \
  --body-file ./sprint_review.html \
  -a ./assets/metrics.pdf \
  -y
```

---

## 7. Provider Automation & DOM Engineering

### Outlook Provider (`auto_mail/providers/outlook.py`)
1. **Compose Detection**: Queries 6+ distinct button selectors (`button[aria-label*="New mail"]`, `button[data-automation-id="newMessageButton"]`, text matching).
2. **Badge Tokenization**: Enters recipient text, then fires CDP Enter (`keyCode: 13`).
3. **Subject Setting**:
   ```python
   # Primary: Native WebBridge fill
   driver.fill(selectors.subject_field, subject)
   # Fallback: React/Angular synthetic setter + events
   ```
4. **Body Setting**: Native WebBridge fill handles contentEditable without triggering browser CSP blocks.
5. **Readiness Report**: Verifies `validPills > 0`, `invalidPills == 0`, `subjectSet == True`, `bodySet == True`.
6. **Dispatch**: Sends native `Ctrl+Enter` shortcut, followed by verification that compose dialog closed.

---

## 8. Data Privacy & PCI-DSS Sanitizer Layer

Implemented in `auto_mail/security/sanitizer.py`:

* **Luhn Algorithm (`is_luhn_valid`)**:
  ```python
  def is_luhn_valid(number_str: str) -> bool:
      digits = [int(c) for c in number_str if c.isdigit()]
      checksum = 0
      reverse_digits = digits[::-1]
      for i, d in enumerate(reverse_digits):
          if i % 2 == 1:
              doubled = d * 2
              checksum += doubled if doubled < 10 else doubled - 9
          else:
              checksum += d
      return checksum % 10 == 0
  ```
* **Cardholder Data Redaction**: Automatically transforms sensitive card numbers (`4111222233334444` → `[REDACTED_CARD_PAN]`).
* **Cryptographic Keys**: Blocks any email containing `-----BEGIN OPENSSH PRIVATE KEY-----` or `-----BEGIN RSA PRIVATE KEY-----`.

---

## 9. Driver & Protocol Abstraction Layer

* **`WebBridgeDriver`**: Talks to real user browser with active cookies and sessions.
* **`PlaywrightDriver`**: Standalone browser instance for automated headless testing.
* **`SMTPDriver`**: Fallback direct socket MTA communication using Python's `smtplib`.

---

*Authored by Roshan Rathore. All rights reserved.*
