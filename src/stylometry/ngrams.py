from collections import Counter

def character_ngrams(text: str, n: int = 3) -> dict:
    text = text.lower()
    grams = [text[i:i+n] for i in range(max(0, len(text)-n+1))]
    counts = Counter(grams)
    total = max(len(grams), 1)
    return {g: c/total for g, c in counts.most_common(500)}
