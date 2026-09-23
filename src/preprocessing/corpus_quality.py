import hashlib

def assess_quality(posts: list, cleaned_texts: list[str], language: str | None, duplicate_ratio: float, duplicates_removed: int = 0, templates_removed: int = 0, contamination_detected: bool = False, corpus_hash: str = "") -> dict:
    """
    Assesses the overall corpus quality and eligibility for stylometric analysis.
    """
    total_posts = len(posts)
    clean_characters = sum(len(text) for text in cleaned_texts)
    
    reasons = []
    eligible = True
    
    if total_posts < 5:
        eligible = False
        reasons.append(f"Insufficient posts: {total_posts} (minimum 5 required)")
        
    if clean_characters < 500:
        eligible = False
        reasons.append(f"Insufficient clean characters: {clean_characters} (minimum 500 required)")
        
    if duplicate_ratio >= 0.5:
        eligible = False
        reasons.append(f"High duplicate ratio: {duplicate_ratio:.2f} (must be < 0.5)")
        
    if not corpus_hash and cleaned_texts:
        hasher = hashlib.sha256()
        for text in cleaned_texts:
            hasher.update(text.encode('utf-8'))
        corpus_hash = hasher.hexdigest()
        
    return {
        "post_count": total_posts,
        "character_count": clean_characters,
        "eligible": eligible,
        "reasons": reasons,
        "duplicates_removed": duplicates_removed,
        "templates_removed": templates_removed,
        "contamination_detected": contamination_detected,
        "language": language,
        "corpus_hash": corpus_hash
    }
