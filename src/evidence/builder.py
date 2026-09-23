def build_evidence(category, explanation, source="persona-analysis", source_url=None, post_ids=None, confidence=0.5):
    return {
        "category": category,
        "source": source,
        "source_url": source_url,
        "post_ids": post_ids or [],
        "explanation": explanation,
        "confidence": max(0.0, min(1.0, confidence))
    }
