import re
import hashlib
import unicodedata

URL_RE = re.compile(r"https?://\S+|www\.\S+", re.I)
PGP_RE = re.compile(r"-----BEGIN PGP.*?-----END PGP.*?-----", re.S)
WALLET_RE = re.compile(r" (?:0x[a-fA-F0-9]{20,}|[13][a-km-zA-HJ-NP-Z1-9]{25,40}) ")
CODE_BLOCK_RE = re.compile(r"```.*?```", re.S)

def clean_text(text: str) -> str:
    """
    Cleans text by removing URLs, PGP blocks, wallet addresses, and code blocks.
    Normalizes whitespace and unicode characters (NFKC).
    """
    text = unicodedata.normalize("NFKC", text)
    text = CODE_BLOCK_RE.sub(" ", text)
    text = PGP_RE.sub(" ", text)
    text = URL_RE.sub(" ", text)
    text = WALLET_RE.sub(" ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def clean_post(text: str) -> tuple[str, str]:
    """
    Cleans a post and returns both the raw text and the cleaned text.
    """
    return text, clean_text(text)

def corpus_hash(texts: list[str]) -> str:
    raw = "\n".join(texts).encode()
    return hashlib.sha256(raw).hexdigest()
