from collections import Counter

def lexical_features(text: str) -> dict:
    words = [w.lower() for w in text.split() if w.strip()]
    n = len(words)
    if not n:
        return {"word_count": 0}
    counts = Counter(words)
    return {
        "word_count": n,
        "unique_words": len(counts),
        "type_token_ratio": len(counts) / n,
        "hapax_ratio": sum(v == 1 for v in counts.values()) / n,
        "avg_word_length": sum(map(len, words)) / n,
        "top_words": counts.most_common(20)
    }
