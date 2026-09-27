"""GitHub Student Developer Pack Verification & Claim Notice."""

from typing import Dict, Any

def generate_student_pack_claim(
    student_name: str,
    email: str,
    github_user: str,
    partner_service: str,
    benefit_description: str
) -> Dict[str, str]:
    """Generates standard partner benefit claim email."""
    subject = f"GitHub Student Developer Pack Claim: {partner_service} Benefit Activation - {github_user}"
    body_html = f"""<div>Dear {partner_service} Student Program Support Team,<br><br>
I am reaching out regarding the activation of my <b>GitHub Student Developer Pack</b> benefits for <b>{partner_service}</b>.<br><br>
<b>Account Details:</b><br>
• Student Name: {student_name}<br>
• Registered Email: {email}<br>
• GitHub Username: <a href="https://github.com/{github_user}">{github_user}</a><br>
• Partner Benefit: {benefit_description}<br><br>
I have successfully verified my student academic status through GitHub Education. Please assist in provisioning the allocated developer credits to my registered account.<br><br>
Thank you for your support of student developers and the open-source community.<br><br>
Sincerely,<br>
<b>{student_name}</b><br>
GitHub: <a href="https://github.com/{github_user}">https://github.com/{github_user}</a>
</div>"""
    return {"subject": subject, "body_html": body_html}
