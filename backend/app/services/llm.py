# backend/app/services/llm.py
from __future__ import annotations

from typing import Literal

from openai import OpenAI

from app.core.config import settings

# Create OpenAI client using the configured API key.
client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
)

LangCode = Literal["en", "si", "ta"]


SYSTEM_INSTRUCTIONS = """
You are Neryx, the multilingual AI assistant for SA Thomson Nerys & Co.,
a real-estate investment and advisory firm operating in Australia, Sri Lanka, and Dubai.

Tone:
- Professional, trustworthy, and investment-focused.
- Clear, concise, and friendly.

Language requirements:
- Always reply in the same language as the user message when possible.
- Supported languages:
  - "en": English
  - "si": Sinhala
  - "ta": Tamil
- If the provided lang code is missing or unknown, auto-detect from the text and reply in that language.

Domain rules:
- You specialise in:
  - Property investment (residential and commercial)
  - Off-the-plan projects and new developments
  - Cashflow, yields, capital growth, and portfolio strategy
- If asked about specific property listings or availability, and you don't have direct data,
  be transparent: explain that this demo version does not yet have live listing data,
  then ask clarifying questions (budget, location, timeline) and give high-level guidance.
- Do NOT invent specific property IDs, prices, or addresses that are not provided.

Style:
- Short paragraphs, bullet points where helpful.
- Avoid over-selling; focus on data-driven, risk-aware investment advice.
""".strip()


def generate_neryx_answer(
    text: str,
    lang: LangCode = "en",
) -> str:
    """
    Call OpenAI Responses API to generate a Neryx reply.

    :param text: user message
    :param lang: language code ("en", "si", "ta")
    :return: plain text answer to show in the chat UI
    """
    if not settings.OPENAI_API_KEY:
        # Fail gracefully with a clear message instead of crashing.
        return (
            "⚠️ Backend configuration issue: OPENAI_API_KEY is not set. "
            "Please notify the site administrator."
        )

    prompt = f"[lang={lang}] {text}".strip()

    response = client.responses.create(
        model=settings.OPENAI_MODEL,
        instructions=SYSTEM_INSTRUCTIONS,
        input=prompt,
    )

    # openai>=2.x exposes a convenience property `.output_text`
    try:
        answer = (response.output_text or "").strip()
    except AttributeError:
        # Fallback parsing in case the SDK ever changes
        try:
            data = response.model_dump()
            outputs = data.get("output", []) or []
            for item in outputs:
                if item.get("type") == "message":
                    for c in item.get("content", []):
                        if c.get("type") == "output_text":
                            return (c.get("text") or "").strip()
            return "Sorry, I couldn't generate a response right now."
        except Exception:
            return "Sorry, I couldn't generate a response right now."

    if not answer:
        return "Sorry, I couldn't generate a response right now."

    return answer
