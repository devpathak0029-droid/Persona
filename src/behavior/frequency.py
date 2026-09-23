def frequency_features(posts: list) -> dict:
    stamps = sorted(p.timestamp for p in posts if p.timestamp)
    if len(stamps) < 2:
        return {"timestamped_posts": len(stamps), "avg_gap_hours": None}
    gaps = [(b-a).total_seconds()/3600 for a,b in zip(stamps, stamps[1:])]
    return {
        "timestamped_posts": len(stamps),
        "avg_gap_hours": sum(gaps)/len(gaps),
        "min_gap_hours": min(gaps),
        "max_gap_hours": max(gaps)
    }
