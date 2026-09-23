import re
from collections import Counter

def spelling_features(text: str) -> dict:
    tokens = re.findall(r"[A-Za-z]+", text)
    misshape = [t for t in tokens if re.search(r"(.)\1\1", t.lower())]
    caps = sum(1 for t in tokens if len(t) > 1 and t.isupper())
    return {
        "all_caps_token_ratio": caps / max(len(tokens), 1),
        "repeated_character_tokens": Counter(x.lower() for x in misshape).most_common(20)
    }
