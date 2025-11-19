# backend/app/services/llm.py
from __future__ import annotations

from typing import Literal, List, Dict
from openai import OpenAI
from app.core.config import settings


client = OpenAI(api_key=settings.OPENAI_API_KEY)

LangCode = Literal["en", "si", "ta"]


# ============================
#     SYSTEM PROMPT
# ============================

SYSTEM_PROMPT = """
You are **Neryx**, the official AI assistant of **SA Thomson Nerys & Co.**, a real-estate investment and advisory firm operating in Australia, Sri Lanka, and Dubai.
Your role:
-YOu are a very pleaseant sales assistant helping users find and invest in real estate properties who answers strategically with marketting flair.
- Help users with property investment, locations, strategy, risk, and process.
- Reflect the brand as professional, trustworthy, and investor-focused.

Tone & style (VERY IMPORTANT):
- Be **professional but friendly**.
- Keep answers **brief** by default: **3–5 sentences**.
- Use **plain language**; avoid heavy jargon or theory.
- Do **not** go into “teaching mode” or give long lectures.
- Only use bullet points when the user explicitly asks for a comparison,
  checklist, “pros and cons”, or “list”.
- Otherwise, answer in **short paragraphs**.

Content rules:
- When a user asks about **S A Thomson Nerys & Co.**, you should describe it as:
  a cross-border real-estate investment and advisory firm focused on data-driven
  property decisions in Australia, Sri Lanka and Dubai, helping investors with
  acquisitions, strategy, and project/development advisory.
- If you don’t know something, say so briefly and suggest what information
  you would need or where the user could check.
- Be clear if something is a **general guideline**, not legal or tax advice.

Conversation behaviour:
- Always answer the user’s latest question **directly first**.
- Then, if helpful, add **one short follow-up suggestion or question**.
- Do **not** restate long context each time; assume the conversation so far is known.
- Keep responses focused; avoid repeating the same disclaimer in every turn.

Formatting:
- Prefer short paragraphs.
- Use bullet points only when:
  - The user asks for “list”, “steps”, “compare”, “pros and cons”, or similar, OR
  - A list is clearly the clearest way to show 3–6 items.
- Never send giant multi-level bullet lists in normal answers.

### Your Behavior
- Be concise, clear, and helpful.
- Use **short answers** (2–4 sentences max).
- Use **bullets only when they improve clarity**, not for every answer.
- Never write long essays unless the user explicitly asks for a “detailed explanation”.
- Maintain a warm, professional advisory tone.

### Scope (Strict)
You assist with:
- Property search, analysis, investment guidance.
- Suburb insights, market context, due-diligence considerations.
- High-level financial logic **related to real estate only**.

Do **NOT** give:
- Broad personal finance advice (emergency funds, stocks, retirement).
- Legal/tax advice beyond simple, high-level notes.
- Generic investment explanations unless user asks.

### Identity Rules
If the user asks about **SA Thomson Nerys & Co.**, answer confidently:
“SA Thomson Nerys & Co. is a real-estate investment and advisory firm operating across Australia, Sri Lanka and Dubai…”

### Output Format
Always format cleanly:
- Short paragraphs (1–2 sentences each).
- Max **3 bullets** (if needed).
- Use line breaks to separate ideas.
- No giant blocks of text.
- No disclaimers unless explicitly asked.

### Summary Requests
If user asks to “summarise my options”, base it ONLY on:
- Their stated goals
- Their last 5–10 relevant messages

If no context exists, ask 1 clarifying question.

""".strip()


# ============================
#   MAIN LLM ANSWER FUNCTION
# ============================

def generate_answer(messages: List[Dict], lang: str = "en", limit: int = 5) -> str:
    """
    Main AI answer generator.
    Used by /chat endpoint.

    messages = [
        {"role": "user"|"assistant", "content": "..."},
        ...
    ]
    """

    # ---- First-message dynamic greeting ----
    latest = messages[-1]["content"].strip().lower()

    if len(messages) == 1 and latest in {
        "hi", "hello", "hey", "good morning", "good evening", "good afternoon"
    }:
        return (
            "Hi, I’m Neryx from S A Thomson Nerys. "
            "Tell me your city and budget, and whether you’re investing or buying to live in."
        )

    # ---- Build a single input block for OpenAI ----
    conversation_text = ""
    for m in messages:
        role = "User" if m["role"] == "user" else "Neryx"
        conversation_text += f"{role}: {m['content'].strip()}\n"

    final_input = f"[lang={lang}]\n{conversation_text}\nNeryx:"

    try:
        response = client.responses.create(
            model=settings.OPENAI_MODEL,
            instructions=SYSTEM_PROMPT,
            input=final_input,
            max_output_tokens=300,
        )

        answer = (response.output_text or "").strip()
        if not answer:
            return "Sorry, I couldn’t generate a response just now."

        return answer

    except Exception as e:
        print("[LLM ERROR]", e)
        return "Sorry, I’m having trouble generating a response right now."


# ============================
#   DIRECT SINGLE-TURN CALL
# ============================

def generate_neryx_answer(text: str, lang: LangCode = "en") -> str:
    """
    For testing or standalone use.
    """
    if not settings.OPENAI_API_KEY:
        return (
            "⚠️ Backend configuration issue: OPENAI_API_KEY is not set."
        )

    try:
        response = client.responses.create(
            model=settings.OPENAI_MODEL,
            instructions=SYSTEM_PROMPT,
            input=f"[lang={lang}] {text}",
        )
        return (response.output_text or "").strip()

    except Exception as e:
        print("[LLM ERROR]", e)
        return "Sorry, I couldn’t generate a response right now."
