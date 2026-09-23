import re

SIGNATURE_RE = re.compile(r"(---\s*\n.*)$", re.S)
SENT_FROM_RE = re.compile(r"(Sent from my.*?)$", re.I | re.S)
POWERED_BY_RE = re.compile(r"(Powered by.*?)$", re.I | re.S)
PGP_HEADER_RE = re.compile(r"-----BEGIN PGP SIGNED MESSAGE-----.*?Hash: [A-Z0-9-]+\s+", re.S)

def detect_templates(text: str) -> dict:
    """
    Detects and removes forum boilerplate, signatures, and templates from the text.
    """
    original_text = text
    removed_segments = []
    has_signature = False
    has_boilerplate = False

    # Remove PGP header
    pgp_match = PGP_HEADER_RE.search(text)
    if pgp_match:
        has_boilerplate = True
        removed_segments.append(pgp_match.group(0))
        text = text[:pgp_match.start()] + text[pgp_match.end():]

    # Remove signatures (---)
    sig_match = SIGNATURE_RE.search(text)
    if sig_match:
        has_signature = True
        removed_segments.append(sig_match.group(0))
        text = text[:sig_match.start()]

    # Remove "Sent from my"
    sent_from_match = SENT_FROM_RE.search(text)
    if sent_from_match:
        has_boilerplate = True
        removed_segments.append(sent_from_match.group(0))
        text = text[:sent_from_match.start()]

    # Remove "Powered by"
    powered_match = POWERED_BY_RE.search(text)
    if powered_match:
        has_boilerplate = True
        removed_segments.append(powered_match.group(0))
        text = text[:powered_match.start()]

    return {
        "has_signature": has_signature,
        "has_boilerplate": has_boilerplate,
        "cleaned_text": text.strip(),
        "removed_segments": removed_segments
    }
