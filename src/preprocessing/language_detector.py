def detect_language(text: str) -> str | None:
    try:
        from langdetect import detect
        return detect(text) if text.strip() else None
    except Exception:
        return None
