import re

def sentence_features(text: str) -> dict:
    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
    lengths = [len(s.split()) for s in sentences]
    if not lengths:
        return {"sentence_count": 0}
    mean = sum(lengths) / len(lengths)
    variance = sum((x - mean) ** 2 for x in lengths) / len(lengths)
    return {
        "sentence_count": len(lengths),
        "mean_sentence_length": mean,
        "min_sentence_length": min(lengths),
        "max_sentence_length": max(lengths),
        "sentence_length_variance": variance
    }
