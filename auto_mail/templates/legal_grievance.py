"""Dual-Jurisdiction Legal Grievance Generator (India & Singapore).

Generates formal legal notices citing:
- India Consumer Protection Act, 2019 (Sections 2(28), 89, 2(47))
- Reserve Bank of India (RBI) e-Mandate and Card Processing Directives
- Singapore Consumer Protection (Fair Trading) Act (CPFTA, Cap. 52A, Part II Section 4)
- False / Deceptive Advertising & Unfair Trade Practices
"""

from typing import Dict, Any, Optional

def generate_dual_jurisdiction_grievance(
    claimant_name: str = "Roshan Rathore",
    registered_email: str = "sgarmy200@outlook.com",
    github_user: str = "roshan-pixel",
    target_platform: str = "Heroku / Salesforce Inc.",
    advertised_offer: str = "$13 USD credit per month for 24 months via GitHub Student Developer Pack",
    error_experienced: str = 'Gateway Address Validation Failure ("Unable to recognize city")',
    charge_amount: str = "USD $1.00 (equivalent to INR ₹95.55)",
    merchant_descriptor: str = "WWW-HEROKUCHARGE-COM",
    project_repo: str = "https://github.com/roshan-pixel/-ledger_web",
    production_domain: str = "dsr7.me"
) -> Dict[str, str]:
    """Generates subject and rich HTML body for a formal dual-jurisdiction legal grievance."""

    subject = f"FORMAL GRIEVANCE: {target_platform} Promotional Benefit Withheld & Unauthorized {charge_amount} Verification Hold | Account: {registered_email}"

    body_html = f"""<div>Dear {target_platform} Support, Executive Leadership & Legal Compliance Directorate,<br><br>
<b>RE: Urgent Service Escalation & Formal Legal Grievance — GitHub Student Developer Pack Promotional Benefit Withheld, Automated Gateway Failure ({error_experienced}), and Unauthorized Financial Deduction | Account: {registered_email}</b><br><br>
I am writing to file a high-priority formal complaint and service escalation concerning my account (registered email: <b>{registered_email}</b>, linked GitHub handle: <b>{github_user}</b>).<br><br>
I am an officially verified student developer under the <b>GitHub Student Developer Pack</b> and an <b>active open-source contributor on GitHub</b> (<a href="https://github.com/{github_user}">https://github.com/{github_user}</a>). I hold citizen and legal standing across both <b>India and Singapore</b>.<br><br>
<hr>
<b>1. UNFAIR PROMOTIONAL ADVERTISING & LACK OF MANDATORY CARD DISCLOSURE:</b><br>
Under the official promotional onboarding material, the platform publicly promises:<br>
<blockquote style="margin: 8px 0; padding: 8px 12px; border-left: 3px solid #79589f; background-color: #f8f9fa;">
<i>"{advertised_offer}"</i>
</blockquote>
The primary promotional onboarding material provides students with the clear representation that authenticating via GitHub immediately unlocks the advertised credits to build and host cloud applications. At no point on the primary landing page is there conspicuous disclosure that students must enter payment card credentials or undergo recurring pre-authorization holds to access their free student benefit.<br><br>
<hr>
<b>2. GATEWAY FAILURE & CONCURRENT UNAUTHORIZED TRANSACTION:</b><br>
After authenticating my verified GitHub account (<b>{github_user}</b>), provisioning was blocked by a mandatory billing verification page.<br><br>
When I submitted my legitimate residential and billing address located in <b>Aizawl, Mizoram, PIN 796009, India</b>:<br>
1) <b>Systemic Validation Defect:</b> The address verification gateway repeatedly rejected the submission with the error banner:<br>
&nbsp;&nbsp;&nbsp;&nbsp;<b>"{error_experienced}"</b><br>
2) <b>Financial Deduction Despite Gateway Failure:</b> Despite rejecting my valid city and failing the verification process, the payment processor (<b>{merchant_descriptor}</b>) initiated a transaction debit of <b>{charge_amount}</b> from my bank account.<br>
3) <b>Contradictory System Notices:</b> Automated platform notifications simultaneously stated <i>"Your credit card is pending verification"</i> followed by <i>"Unable to verify credit card"</i>, leaving my student credit blocked while funds remain debited/held.<br>
4) <b>Unmonitored Communication Channels:</b> Standard billing inquiry aliases returned automated bounces declaring the address unmonitored, necessitating this multi-stakeholder formal escalation.<br><br>
<hr>
<b>3. VIOLATION OF STATUTORY CONSUMER PROTECTION LAWS (INDIA & SINGAPORE):</b><br>
Withholding advertised promotional benefits, failing to disclose mandatory payment collection upfront, and executing financial deductions during an aborted address validation constitutes actionable unfair trade practices under dual applicable jurisdictions:<br><br>
• <b>India — Consumer Protection Act, 2019:</b><br>
&nbsp;&nbsp;- <i>Section 2(28) & Section 89:</i> Strict prohibition against misleading advertisements and deceptive trade inducements.<br>
&nbsp;&nbsp;- <i>Section 2(47):</i> Unfair trade practices, including withholding goods or services rightfully promised and failure to provide standard service.<br>
&nbsp;&nbsp;- <i>Reserve Bank of India (RBI) Directives:</i> Rules governing merchant pre-authorization holds, explicit customer consent, and mandatory e-mandate validation integrity.<br><br>
• <b>Singapore — Consumer Protection (Fair Trading) Act (CPFTA, Cap. 52A):</b><br>
&nbsp;&nbsp;- <i>Part II, Section 4:</i> Unfair practice to make false claims or deceptive statements regarding the terms, price, or availability of services or promotional gifts.<br><br>
<hr>
<b>4. PLANNED OPEN-SOURCE WORKLOAD & ARCHITECTURE:</b><br>
I am actively developing and deploying an open-source accounting and enterprise ledger system:<br>
• <b>Repository:</b> Ledger Web (<a href="{project_repo}">{project_repo}</a>)<br>
• <b>Architecture:</b> Python 3.13, Flask, Gunicorn, SQLite, Google Sheets synchronization, and async task workers.<br>
• <b>Target Custom Domain:</b> <b>{production_domain}</b><br><br>
<hr>
<b>5. DEMANDED CORRECTIVE ACTIONS:</b><br>
1) <b>Manual Credit Provisioning:</b> Manually bypass the flawed automated validation barrier and immediately allocate the advertised student platform credit to account <b>{registered_email}</b>.<br>
2) <b>Immediate Transaction Reversal:</b> Provide immediate written confirmation of the full release and reversal of the <b>{charge_amount}</b> hold debited by {merchant_descriptor}.<br>
3) <b>Address Database Correction:</b> Patch the address verification engine to recognize legitimate Indian capital cities, states, and postal codes (specifically <b>Aizawl, Mizoram, 796009</b>) so that international students are not systematically disenfranchised.<br><br>
<i>Note on Data Privacy: In strict compliance with global PCI-DSS and data minimization standards, no sensitive payment card numbers, CVVs, or personal identity photographs are transmitted via this unencrypted email. Full bank transaction logs and billing screenshots are securely preserved and available upon request via verified support ticket.</i><br><br>
Respectfully submitted,<br><br>
<b>{claimant_name}</b><br>
Verified Student Developer & Open-Source Contributor (GitHub: <b>{github_user}</b>)<br>
Registered Account: {registered_email}<br>
Open Source Profile: <a href="https://github.com/{github_user}">https://github.com/{github_user}</a><br>
Production Domain: <a href="https://{production_domain}">https://{production_domain}</a>
</div>"""

    return {"subject": subject, "body_html": body_html}
