# backend/app/services/mailer.py

from app.core.config import get_settings
import sendgrid
from sendgrid.helpers.mail import Mail


def _client():
    s = get_settings()
    if not s.SENDGRID_API_KEY:
        print("[DEV MODE] SENDGRID_API_KEY not set — emails will not be sent.")
        return None
    return sendgrid.SendGridAPIClient(api_key=s.SENDGRID_API_KEY)


def send_sales_alert(user_name: str, user_email: str, user_phone: str | None):
    s = get_settings()
    subject = "📩 New Lead from Chatbot"
    body = f"""
New chatbot lead:

Name: {user_name}
Email: {user_email}
Phone: {user_phone or '(not provided)'}

Source: Neryx AI Assistant
"""
    client = _client()
    if not client:
        print("[SALES ALERT DEV]", subject, body)
        return

    msg = Mail(
        from_email=s.WELCOME_EMAIL_FROM,
        to_emails=s.SALES_ALERT_TO,
        subject=subject,
        plain_text_content=body,
    )
    client.send(msg)


def send_user_welcome_email(user_email: str, user_name: str | None = None):
    s = get_settings()
    subject = "Welcome to SA Thomson Nerys"
    body = f"""
Hi {user_name or ''},

Thank you for contacting SA Thomson Nerys.
One of our advisors will follow up shortly.

Regards,
SA Thomson Nerys & Co.
"""

    client = _client()
    if not client:
        print("[WELCOME EMAIL DEV]", subject, body)
        return

    msg = Mail(
        from_email=s.WELCOME_EMAIL_FROM,
        to_emails=user_email,
        subject=subject,
        plain_text_content=body,
    )
    client.send(msg)
