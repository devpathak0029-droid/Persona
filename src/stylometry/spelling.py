import re
from collections import Counter

def spelling_features(text: str) -> dict:
    tokens = re.findall(r"[A-Za-z]+", text)
    misshape = [t for t in tokens if re.search(r"(.)\1\1", t.lower())]
    caps = sum(1 for t in tokens if len(t) > 1 and t.isupper())
    
    words = text.lower().split()
    abbrev_list = {'ur', 'u', 'r', 'w/', 'bc', 'imo', 'tbh', 'afaik', 'iirc', 'fyi', 'btw', 'smh', 'lol', 'lmao', 'rofl'}
    abbrev_count = sum(1 for w in words if w in abbrev_list or w.strip('.,!?') in abbrev_list)
    abbrev_ratio = abbrev_count / max(len(words), 1)
    
    apostrophe_pairs = {
        "don't": 0, "dont": 0,
        "can't": 0, "cant": 0,
        "it's": 0, "its": 0,
        "i'm": 0, "im": 0,
        "you're": 0, "your": 0,
        "they're": 0, "theyre": 0,
        "we're": 0, "were": 0,
        "isn't": 0, "isnt": 0,
        "aren't": 0, "arent": 0,
        "won't": 0, "wont": 0
    }
    for w in words:
        clean_w = w.strip('.,!?')
        if clean_w in apostrophe_pairs:
            apostrophe_pairs[clean_w] += 1
            
    mixed_case = sum(1 for t in tokens if len(t) > 1 and t[0].islower() and any(c.isupper() for c in t[1:]))
    
    return {
        "all_caps_token_ratio": caps / max(len(tokens), 1),
        "repeated_character_tokens": Counter(x.lower() for x in misshape).most_common(20),
        "abbreviation_count": abbrev_count,
        "abbreviation_ratio": abbrev_ratio,
        "apostrophe_usage": apostrophe_pairs,
        "mixed_case_tokens": mixed_case
    }
