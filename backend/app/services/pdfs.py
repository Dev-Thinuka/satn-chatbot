# app/services/pdfs.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from typing import List, Dict
from io import BytesIO
from typing import Iterable
from reportlab.lib.units import mm

def make_chat_summary_pdf(name: str, email: str, message: str, reply: str) -> bytes:
    """(Legacy) Single-turn summary."""
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    c.setTitle("Chat Summary")
    y = 800
    for line in [
        "SA Thomson Nerys — Chat Summary",
        f"Name: {name}",
        f"Email: {email}",
        "", "User Message:", message, "", "Chatbot Reply:", reply,
    ]:
        c.drawString(50, y, line); y -= 18
    c.showPage(); c.save()
    return buf.getvalue()

def _wrap_text(text: str, width_chars: int = 100) -> Iterable[str]:
    import textwrap
    return textwrap.wrap(text.replace("\r", " ").replace("\n", " "), width=width_chars)

def make_chat_transcript_pdf(name: str, email: str, messages: list[dict], properties: list[dict] | None = None) -> bytes:
    """Simple, reliable PDF builder for chat transcript + optional properties."""
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    W, H = A4
    x = 20 * mm
    y = H - 25 * mm

    c.setTitle("SA Thomson Nerys — Chat Summary")
    c.setFont("Helvetica-Bold", 14)
    c.drawString(x, y, "SA Thomson Nerys — Chat Summary"); y -= 9 * mm

    c.setFont("Helvetica", 10)
    c.drawString(x, y, f"Name: {name}   Email: {email}"); y -= 7 * mm
    c.line(x, y, W - x, y); y -= 6 * mm

    c.setFont("Helvetica", 11)
    c.drawString(x, y, "Conversation:"); y -= 6 * mm
    c.setFont("Helvetica", 10)

    for m in messages:
        role = "You" if m.get("role") == "user" else "Assistant"
        for line in _wrap_text(f"{role}: {m.get('text','')}"):
            if y < 20 * mm:
                c.showPage(); y = H - 20 * mm; c.setFont("Helvetica", 10)
            c.drawString(x, y, line); y -= 5 * mm
        y -= 2 * mm

    if properties:
        y -= 4 * mm
        c.setFont("Helvetica", 11); c.drawString(x, y, "Properties:"); y -= 6 * mm
        c.setFont("Helvetica", 10)
        for p in properties:
            title = p.get("title", "Property")
            price = p.get("price")
            loc = p.get("location")
            line = f"• {title}"
            if price is not None: line += f" — {price}"
            if loc: line += f" — {loc}"
            for l in _wrap_text(line, 95):
                if y < 20 * mm:
                    c.showPage(); y = H - 20 * mm; c.setFont("Helvetica", 10)
                c.drawString(x, y, l); y -= 5 * mm
            y -= 1 * mm

    c.showPage(); c.save()
    return buf.getvalue()
