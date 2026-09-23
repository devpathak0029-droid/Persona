import statistics
from typing import Dict, Any

def frequency_features(posts: list) -> Dict[str, Any]:
    stamps = sorted(p.timestamp for p in posts if p.timestamp)
    
    if len(stamps) < 2:
        res = {
            "timestamped_posts": len(stamps), 
            "avg_gap_hours": None,
            "min_gap_hours": None,
            "max_gap_hours": None,
            "median_gap_hours": None,
            "posts_per_day": None,
            "posts_per_week": None,
            "total_active_days": len(set(s.date() for s in stamps)),
            "total_span_days": 0
        }
        return res
        
    gaps = [(b-a).total_seconds()/3600 for a,b in zip(stamps, stamps[1:])]
    
    total_span = stamps[-1] - stamps[0]
    total_span_days = total_span.days + (total_span.seconds / 86400)
    total_span_days_clamped = max(total_span_days, 1.0) # Avoid division by zero
    
    posts_per_day = len(stamps) / total_span_days_clamped
    posts_per_week = posts_per_day * 7
    active_days = len(set(s.date() for s in stamps))
    
    return {
        "timestamped_posts": len(stamps),
        "avg_gap_hours": sum(gaps)/len(gaps),
        "min_gap_hours": min(gaps),
        "max_gap_hours": max(gaps),
        "median_gap_hours": statistics.median(gaps) if gaps else None,
        "posts_per_day": posts_per_day,
        "posts_per_week": posts_per_week,
        "total_active_days": active_days,
        "total_span_days": total_span.days
    }
