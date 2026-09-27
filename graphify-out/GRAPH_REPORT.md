# Graph Report - AUTO-MATIC-MAIL-AGENT-  (2026-09-27)

## Corpus Check
- 34 files · ~14,487 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 408 nodes · 576 edges · 42 communities (18 shown, 24 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 69 edges (avg confidence: 0.7)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `68685529`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]

## God Nodes (most connected - your core abstractions)
1. `WebBridgeDriver` - 23 edges
2. `OutlookProvider` - 23 edges
3. `GmailProvider` - 21 edges
4. `PlaywrightDriver` - 17 edges
5. `MockDriver` - 17 edges
6. `Recipient` - 16 edges
7. `MailAgent` - 15 edges
8. `EmailMessage` - 15 edges
9. `SMTPDriver` - 15 edges
10. `MailAgentError` - 13 edges

## Surprising Connections (you probably didn't know these)
- `Colors` --uses--> `WebBridgeDriver`  [INFERRED]
  send_outlook.py → auto_mail/drivers/webbridge.py
- `Colors` --uses--> `OutlookProvider`  [INFERRED]
  send_outlook.py → auto_mail/providers/outlook.py
- `Colors` --uses--> `RecipientRole`  [INFERRED]
  send_outlook.py → auto_mail/models.py
- `send_mail()` --calls--> `assert_payload_is_safe()`  [INFERRED]
  send_outlook.py → auto_mail/security/sanitizer.py
- `send_mail()` --calls--> `WebBridgeDriver`  [INFERRED]
  send_outlook.py → auto_mail/drivers/webbridge.py

## Communities (42 total, 24 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.07
Nodes (17): main(), Autonomous Mail Agent Orchestrator.  High-level interface coordinating drivers,, CLI entrypoint for auto-mail agent., DataSanitizationError, Custom exceptions for the Mail Agent framework., Raised when sensitive data (e.g. credit card PAN or CVV) is detected in payload., AUTO-MATIC-MAIL-AGENT: Autonomous Email Dispatch & Management Agent for Outlook, ProviderType (+9 more)

### Community 1 - "Community 1"
Cohesion: 0.09
Nodes (9): ABC, BaseMailDriver, Base driver interface for mail automation., Abstract base class for all browser and protocol drivers., Low-level Chrome DevTools Protocol (CDP) Controller.  Handles trusted synthetic, Automation and protocol drivers for mail clients., Kimi WebBridge Driver implementation.  Communicates with the user's active brows, BaseMailProvider (+1 more)

### Community 2 - "Community 2"
Cohesion: 0.07
Nodes (32): AgentConfig, GmailSelectors, OutlookSelectors, Configuration management for Auto-Matic-Mail-Agent., DOM selectors for Microsoft Outlook Web (live.com / office.com)., DOM selectors for Google Gmail Web., Global configuration settings for Mail Agent., Configuration for Kimi WebBridge daemon. (+24 more)

### Community 3 - "Community 3"
Cohesion: 0.08
Nodes (21): DriverConnectionError, Raised when connecting to automation daemon (WebBridge/CDP) fails., CDPController, Helper to construct and execute standard CDP payloads., Focuses element and inserts text., Fills input, textarea, or contenteditable editor via native WebBridge fill tool., Sends native Enter key via CDP to tokenize pills/chips., Sends key combinations such as Ctrl+Enter. (+13 more)

### Community 4 - "Community 4"
Cohesion: 0.12
Nodes (20): Validates, prepares, and dispatches an email message.          Args:, NamedTuple, Security and privacy sanitation subsystem., assert_payload_is_safe(), DataSanitizer, is_luhn_valid(), Privacy and PCI-DSS Data Sanitizer.  Enforces zero-credential leakage by scannin, Detects and redacts sensitive financial and authentication data. (+12 more)

### Community 5 - "Community 5"
Cohesion: 0.07
Nodes (27): 1. Interactive Mode, 1. System Architecture Diagram, 2. Core Engineering Highlights, 2. Direct CLI Command, 3. End-to-End Sequence Flow, 4. Graphify Knowledge Graph & Codebase Navigation, 5. Complete Python Source File Index & Specifications, 6. One-Shot Outlook Mail Dispatcher (`send_outlook.py`) (+19 more)

### Community 6 - "Community 6"
Cohesion: 0.07
Nodes (17): MailAgent, Master orchestrator for autonomous mail operations., Instantiates driver based on configuration., Returns provider engine instance for the driver., DeliveryFailedError, MailAgentError, Raised when email submission fails or returns an unrecoverable bounce/error., Base exception for all auto-mail agent errors. (+9 more)

### Community 7 - "Community 7"
Cohesion: 0.06
Nodes (35): 1. CDP-Powered Native Recipient Tokenization, 1. Prerequisites, 2. ⚡ One-Shot Outlook Mail Dispatcher (`send_outlook.py`), 2. Running Diagnostic Pill/Chip Validation, 2. Zero-Leakage Privacy & PCI-DSS Data Sanitizer, 3. Active Browser Session Borrowing via Kimi WebBridge, 3. Programmatic Python API, 3. Running Diagnostic Pill/Chip Validation (+27 more)

### Community 8 - "Community 8"
Cohesion: 0.14
Nodes (10): BaseMailProvider, Cross-Verification Engine: Outlook <-> Gmail.  Dispatches an email:   1. From Mi, run_cross_verification(), OutlookProvider, Automation engine for Microsoft Outlook Web., Uploads one or more files to the Outlook email draft., Uploads one or more files to the Outlook email draft., Navigates to Outlook Web inbox. (+2 more)

### Community 9 - "Community 9"
Cohesion: 0.22
Nodes (4): PlaywrightDriver, Direct Playwright automation driver (standalone / CI environments)., Initializes playwright browser context if not passed., Closes browser context and playwright session.

### Community 10 - "Community 10"
Cohesion: 0.15
Nodes (9): Example: Sending a Formal Dual-Jurisdiction Legal Grievance via Outlook Web., run(), Templates for legal notices, consumer grievances, and developer claims., generate_dual_jurisdiction_grievance(), Dual-Jurisdiction Legal Grievance Generator (India & Singapore).  Generates form, Generates subject and rich HTML body for a formal dual-jurisdiction legal grieva, generate_student_pack_claim(), GitHub Student Developer Pack Verification & Claim Notice. (+1 more)

### Community 11 - "Community 11"
Cohesion: 0.15
Nodes (9): GmailProvider, Populates To, Cc, and Bcc in Gmail., Automation engine for Google Gmail Web., Uploads files to Gmail draft., Uploads files to Gmail draft., Verifies 'Message sent' toast or compose dialog close., Navigates to Gmail inbox., Verifies 'Message sent' toast or compose dialog close. (+1 more)

### Community 12 - "Community 12"
Cohesion: 0.14
Nodes (11): ComposeTimeoutError, ElementInteractionError, Raised when the mail client compose dialog or elements do not appear within time, Raised when clicking, typing, or dispatching events to a DOM node fails., Sets subject line in Gmail compose., Injects rich HTML into Gmail message body with TrustedHTML compatibility., Opens Gmail compose popup if not already present., Injects subject line using native fill (primary) then JS fallback. (+3 more)

### Community 13 - "Community 13"
Cohesion: 0.29
Nodes (10): get_driver(), main(), print_summary(), Diagnostic script to verify Outlook validPill and Gmail chip creation.  Validate, Tests Gmail recipient chip creation and validates native chip tokenization., Prints a structured summary table of all test runs., Instantiates the requested automation driver., Tests Outlook Web recipient pill creation and checks for red invalidPills. (+2 more)

### Community 14 - "Community 14"
Cohesion: 0.21
Nodes (6): MockDriver, Tests for Outlook and Gmail provider orchestration with MockDriver., test_gmail_provider_recipient_setting(), test_gmail_readiness_verification(), test_outlook_provider_recipient_setting(), test_outlook_readiness_verification()

### Community 16 - "Community 16"
Cohesion: 0.29
Nodes (4): Raised when an email recipient fails syntax or platform pill/chip validation., RecipientValidationError, Populates To, Cc, and Bcc fields with verified tokenized pills., Inserts an email and commits it with CDP Enter to form a native validPill.

### Community 39 - "Community 39"
Cohesion: 0.33
Nodes (4): Inspects Gmail compose state prior to sending., Sends email in Gmail via Ctrl+Enter or Send button., Inspects Gmail compose state prior to sending., Sends email in Gmail via Ctrl+Enter or Send button.

### Community 40 - "Community 40"
Cohesion: 0.33
Nodes (4): Inspects recipient pills, subject, and editor state., Sends email using Send button or CDP Ctrl+Enter shortcut., Inspects recipient pills, subject, and editor state., Sends email using Send button or CDP Ctrl+Enter shortcut.

## Knowledge Gaps
- **30 isolated node(s):** `📑 Document Structure`, `code:mermaid (flowchart TD)`, `I. Chrome DevTools Protocol (CDP) Virtual Keycode Tokenization`, `II. Resilient Subject & ContentEditable Injection (TrustedHTML & React Setters)`, `III. Zero-Leakage Privacy & PCI-DSS Data Sanitizer` (+25 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `WebBridgeDriver` connect `Community 3` to `Community 1`, `Community 2`, `Community 6`, `Community 8`, `Community 13`?**
  _High betweenness centrality (0.116) - this node is a cross-community bridge._
- **Why does `OutlookProvider` connect `Community 8` to `Community 0`, `Community 1`, `Community 2`, `Community 6`, `Community 40`, `Community 12`, `Community 13`, `Community 14`, `Community 16`?**
  _High betweenness centrality (0.103) - this node is a cross-community bridge._
- **Why does `GmailProvider` connect `Community 11` to `Community 0`, `Community 1`, `Community 2`, `Community 6`, `Community 39`, `Community 8`, `Community 12`, `Community 13`, `Community 14`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `WebBridgeDriver` (e.g. with `Colors` and `BaseMailDriver`) actually correct?**
  _`WebBridgeDriver` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `OutlookProvider` (e.g. with `Colors` and `BaseMailProvider`) actually correct?**
  _`OutlookProvider` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `GmailProvider` (e.g. with `BaseMailProvider` and `MockDriver`) actually correct?**
  _`GmailProvider` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `PlaywrightDriver` (e.g. with `BaseMailDriver` and `get_driver()`) actually correct?**
  _`PlaywrightDriver` has 2 INFERRED edges - model-reasoned connections that need verification._