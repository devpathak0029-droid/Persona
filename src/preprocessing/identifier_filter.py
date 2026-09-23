import re

MENTION_RE = re.compile(r"@\w+")
PGP_KEY_ID_RE = re.compile(r"0x[a-fA-F0-9]{8,16}")

def filter_identifiers(text: str, known_handles: list[str] = None) -> str:
    """
    Filters out identifiers that could contaminate stylometric analysis.
    Removes @mentions, PGP key IDs, and known handles.
    """
    text = MENTION_RE.sub(" ", text)
    text = PGP_KEY_ID_RE.sub(" ", text)
    
    if known_handles:
        for handle in known_handles:
            # Word boundary matching for handles
            escaped_handle = re.escape(handle)
            # Use case-insensitive matching for handles
            handle_re = re.compile(r"\b" + escaped_handle + r"\b", re.IGNORECASE)
            text = handle_re.sub(" ", text)
            
    # Clean up multiple spaces that might have been introduced
    text = re.sub(r"\s+", " ", text)
    return text.strip()
