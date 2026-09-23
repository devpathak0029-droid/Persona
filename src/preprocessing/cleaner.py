import re
import hashlib

URL_RE = re.compile(r"https?://\S+|www\.\S+", re.I)
PGP_RE = re.compile(r"-----BEGIN PGP.*?-----END PGP.*?-----", re.S)
WALLET_RE = re.compile(r"(?:0x[a-fA-F0-9]{20,}|[13][a-km-zA-HJ-NP-Z1-9]{25,40})")

def clean_text(text: str) -> str:
    text = PGP_RE.sub(" ", text)
    text = URL_RE.sub(" ", text)
    text = WALLET_RE.sub(" ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def corpus_hash(texts: list[str]) -> str:
    raw = "\n".join(texts).encode()
    return hashlib.sha256(raw).hexdigest()
