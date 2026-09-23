from collections import Counter

PUNCT = ".,!?;:'\"-()[]{}"

def punctuation_features(text: str) -> dict:
    counts = Counter(c for c in text if c in PUNCT)
    n = max(len(text), 1)
    return {c: counts[c] / n for c in PUNCT}
