from langdetect import detect
def detect_lang(text: str) -> str:
    try:
        code = detect(text)
        if code.startswith("si"): return "si"
        if code.startswith("ta"): return "ta"
        return "en"
    except Exception:
        return "en"
def translate_to_en(text: str, _src: str) -> str:
    return text
def translate_from_en(text: str, target: str) -> str:
    return text
