from ..core.config import get_settings
def send_sales_alert(user_name: str, user_email: str, user_phone: str | None):
    s = get_settings()
    print(f"[SALES ALERT] New lead: {user_name} <{user_email}> {user_phone or ''} -> {s.sales_alert_to}")
def send_pdf_summary(to_email: str, pdf_bytes: bytes):
    print(f"[MAIL] Sent PDF summary to {to_email} ({len(pdf_bytes)} bytes)")
