# Graph Report - AUTO-MATIC-MAIL-AGENT-  (2026-09-27)

## Corpus Check
- 30 files · ~9,649 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 343 nodes · 486 edges · 36 communities (13 shown, 23 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 52 edges (avg confidence: 0.7)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d86313ca`
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
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 15|Community 15]]
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

## God Nodes (most connected - your core abstractions)
1. `GmailProvider` - 20 edges
2. `OutlookProvider` - 20 edges
3. `WebBridgeDriver` - 19 edges
4. `PlaywrightDriver` - 17 edges
5. `MockDriver` - 17 edges
6. `MailAgent` - 15 edges
7. `SMTPDriver` - 15 edges
8. `MailAgentError` - 13 edges
9. `Recipient` - 13 edges
10. `EmailMessage` - 13 edges

## Surprising Connections (you probably didn't know these)
- `run()` --calls--> `MailAgent`  [INFERRED]
  examples/send_gmail_notice.py → auto_mail/agent.py
- `run()` --calls--> `MailAgent`  [INFERRED]
  examples/send_outlook_grievance.py → auto_mail/agent.py
- `MockDriver` --uses--> `OutlookSelectors`  [INFERRED]
  tests/test_providers.py → auto_mail/config.py
- `MockDriver` --uses--> `GmailSelectors`  [INFERRED]
  tests/test_providers.py → auto_mail/config.py
- `MockDriver` --uses--> `RecipientRole`  [INFERRED]
  tests/test_providers.py → auto_mail/models.py

## Communities (36 total, 23 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.09
Nodes (12): Autonomous Mail Agent Orchestrator.  High-level interface coordinating drivers,, Custom exceptions for the Mail Agent framework., AUTO-MATIC-MAIL-AGENT: Autonomous Email Dispatch & Management Agent for Outlook, Data models and abstractions for Mail Agent., Low-level Chrome DevTools Protocol (CDP) Controller.  Handles trusted synthetic, Automation and protocol drivers for mail clients., Playwright Driver implementation for standalone browser execution., Standard SMTP Protocol Driver fallback. (+4 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (7): ABC, BaseMailDriver, Base driver interface for mail automation., Abstract base class for all browser and protocol drivers., BaseMailProvider, Abstract Base Provider for Web Mail Clients., Abstract base class for Outlook, Gmail, and other webmail providers.

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (24): AgentConfig, GmailSelectors, OutlookSelectors, Configuration management for Auto-Matic-Mail-Agent., DOM selectors for Microsoft Outlook Web (live.com / office.com)., DOM selectors for Google Gmail Web., Global configuration settings for Mail Agent., Configuration for Kimi WebBridge daemon. (+16 more)

### Community 3 - "Community 3"
Cohesion: 0.09
Nodes (18): DriverConnectionError, Raised when connecting to automation daemon (WebBridge/CDP) fails., BaseMailDriver, CDPController, Helper to construct and execute standard CDP payloads., Focuses element and inserts text., Sends native Enter key via CDP to tokenize pills/chips., Sends key combinations such as Ctrl+Enter. (+10 more)

### Community 4 - "Community 4"
Cohesion: 0.10
Nodes (24): DataSanitizationError, Raised when sensitive data (e.g. credit card PAN or CVV) is detected in payload., ProviderType, RecipientRole, Enum, NamedTuple, Security and privacy sanitation subsystem., assert_payload_is_safe() (+16 more)

### Community 5 - "Community 5"
Cohesion: 0.16
Nodes (12): MailAgent, main(), CLI entrypoint for auto-mail agent., Master orchestrator for autonomous mail operations., Instantiates driver based on configuration., Returns provider engine instance for the driver., Validates, prepares, and dispatches an email message.          Args:, MailAgentError (+4 more)

### Community 6 - "Community 6"
Cohesion: 0.13
Nodes (5): DeliveryFailedError, Raised when email submission fails or returns an unrecoverable bounce/error., Direct SMTP email dispatch driver., Sends EmailMessage via SMTP., SMTPDriver

### Community 7 - "Community 7"
Cohesion: 0.07
Nodes (29): 1. CDP-Powered Native Recipient Tokenization, 1. Prerequisites, 2. Running Diagnostic Pill/Chip Validation, 2. Zero-Leakage Privacy & PCI-DSS Data Sanitizer, 3. Active Browser Session Borrowing via Kimi WebBridge, 3. Programmatic Python API, 4. Command-Line Interface (CLI), 4. Dual-Jurisdiction Statutory Grievance Generator (+21 more)

### Community 8 - "Community 8"
Cohesion: 0.10
Nodes (15): ElementInteractionError, Raised when clicking, typing, or dispatching events to a DOM node fails., BaseMailProvider, OutlookProvider, Populates To, Cc, and Bcc fields with verified tokenized pills., Injects subject line and triggers event bubbling., Automation engine for Microsoft Outlook Web., Injects rich HTML into Outlook's contentEditable editor. (+7 more)

### Community 9 - "Community 9"
Cohesion: 0.22
Nodes (4): PlaywrightDriver, Direct Playwright automation driver (standalone / CI environments)., Initializes playwright browser context if not passed., Closes browser context and playwright session.

### Community 10 - "Community 10"
Cohesion: 0.15
Nodes (9): Example: Sending a Formal Dual-Jurisdiction Legal Grievance via Outlook Web., run(), Templates for legal notices, consumer grievances, and developer claims., generate_dual_jurisdiction_grievance(), Dual-Jurisdiction Legal Grievance Generator (India & Singapore).  Generates form, Generates subject and rich HTML body for a formal dual-jurisdiction legal grieva, generate_student_pack_claim(), GitHub Student Developer Pack Verification & Claim Notice. (+1 more)

### Community 11 - "Community 11"
Cohesion: 0.06
Nodes (21): ComposeTimeoutError, Raised when an email recipient fails syntax or platform pill/chip validation., Raised when the mail client compose dialog or elements do not appear within time, RecipientValidationError, GmailProvider, Populates To, Cc, and Bcc in Gmail., Sets subject line in Gmail compose., Automation engine for Google Gmail Web. (+13 more)

### Community 13 - "Community 13"
Cohesion: 0.29
Nodes (10): get_driver(), main(), print_summary(), Diagnostic script to verify Outlook validPill and Gmail chip creation.  Validate, Tests Gmail recipient chip creation and validates native chip tokenization., Prints a structured summary table of all test runs., Instantiates the requested automation driver., Tests Outlook Web recipient pill creation and checks for red invalidPills. (+2 more)

## Knowledge Gaps
- **18 isolated node(s):** `📌 Table of Contents`, `code:mermaid (flowchart TD)`, `1. CDP-Powered Native Recipient Tokenization`, `2. Zero-Leakage Privacy & PCI-DSS Data Sanitizer`, `3. Active Browser Session Borrowing via Kimi WebBridge` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MailAgent` connect `Community 5` to `Community 0`, `Community 2`, `Community 10`, `Community 4`?**
  _High betweenness centrality (0.114) - this node is a cross-community bridge._
- **Why does `GmailProvider` connect `Community 11` to `Community 0`, `Community 1`, `Community 2`, `Community 5`, `Community 8`, `Community 13`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Why does `OutlookProvider` connect `Community 8` to `Community 0`, `Community 1`, `Community 2`, `Community 5`, `Community 11`, `Community 13`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `GmailProvider` (e.g. with `BaseMailProvider` and `MockDriver`) actually correct?**
  _`GmailProvider` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `OutlookProvider` (e.g. with `BaseMailProvider` and `MockDriver`) actually correct?**
  _`OutlookProvider` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `WebBridgeDriver` (e.g. with `BaseMailDriver` and `CDPController`) actually correct?**
  _`WebBridgeDriver` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `PlaywrightDriver` (e.g. with `BaseMailDriver` and `get_driver()`) actually correct?**
  _`PlaywrightDriver` has 2 INFERRED edges - model-reasoned connections that need verification._