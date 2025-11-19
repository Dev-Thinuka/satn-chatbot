import os
from typing import Optional

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
WELCOME_TEMPLATE_ID = os.getenv("SENDGRID_WELCOME_TEMPLATE_ID")
FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL", "sales@sathomson.com.au")


def send_welcome_email(
    to_email: str,
    first_name: Optional[str],
    last_name: Optional[str],
) -> None:
    """
    Send the 'Welcome to S A Thomson Nerys' email using the dynamic template.
    Does nothing if configuration is missing.
    """
    if not SENDGRID_API_KEY or not WELCOME_TEMPLATE_ID:
        # Optionally log here, but don't crash the app.
        return

    # Normalise values
    first_name_val = first_name or ""
    last_name_val = last_name or ""

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
    )
    message.template_id = WELCOME_TEMPLATE_ID
    message.dynamic_template_data = {
        "first_name": first_name_val,
        "last_name": last_name_val,
    }

    sg = SendGridAPIClient(SENDGRID_API_KEY)
    sg.send(message)
