# backend/app/services/email_utils.py
import os
import smtplib
from email.message import EmailMessage
from typing import Optional


SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER or "no-reply@sathomson.com.au")

SALES_EMAIL = os.getenv("SALES_EMAIL", "sales@sathomson.com.au")


def _send_email(to_addr: str, subject: str, body: str) -> None:
  if not SMTP_HOST or not to_addr:
    # In dev, silently skip to avoid crashes if email is not configured
    return

  msg = EmailMessage()
  msg["From"] = SMTP_FROM
  msg["To"] = to_addr
  msg["Subject"] = subject
  msg.set_content(body)

  with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
    server.starttls()
    if SMTP_USER and SMTP_PASS:
      server.login(SMTP_USER, SMTP_PASS)
    server.send_message(msg)


def send_lead_emails(name: str, email: str, phone: Optional[str], source: str) -> None:
  # Email to lead
  lead_body = f"""
Hi {name or "there"},

Thank you for reaching out to S A Thomson Nerys & Co. via our website assistant.

One of our advisers will review your enquiry and contact you shortly.

Details we received:
- Email: {email}
- Phone: {phone or "not provided"}
- Source: {source}

Kind regards,
S A Thomson Nerys & Co.
"""

  _send_email(email, "Thank you for contacting S A Thomson Nerys & Co.", lead_body)

  # Notification to sales
  sales_body = f"""
New website chat lead captured.

Name:  {name or "N/A"}
Email: {email}
Phone: {phone or "N/A"}
Source: {source}

You can now follow up with this contact.
"""

  _send_email(SALES_EMAIL, "New SA Thomson Nerys website chat lead", sales_body)
