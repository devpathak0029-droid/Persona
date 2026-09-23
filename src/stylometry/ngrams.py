from collections import Counter

def character_ngrams(text: str, n: int = 3, top_k: int = 200) -> dict:
    text = text.lower()
    grams = [text[i:i+n] for i in range(max(0, len(text)-n+1))]
    counts = Counter(grams)
    total = max(len(grams), 1)
    return {g: c/total for g, c in counts.most_common(top_k)}

def multi_ngrams(text: str) -> dict:
    return {
        "3gram": character_ngrams(text, n=3, top_k=100),
        "4gram": character_ngrams(text, n=4, top_k=100),
        "5gram": character_ngrams(text, n=5, top_k=100)
    }
