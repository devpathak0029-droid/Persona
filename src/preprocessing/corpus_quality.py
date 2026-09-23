def assess_quality(posts: list, cleaned_texts: list[str], language: str | None, duplicate_ratio: float) -> dict:
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
        
    return {
        "posts": total_posts,
        "clean_characters": clean_characters,
        "language": language,
        "duplicate_ratio": duplicate_ratio,
        "eligible": eligible,
        "reasons": reasons
    }
