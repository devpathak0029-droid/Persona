import math
from collections import Counter
from typing import Dict, Any

def temporal_features(posts: list) -> Dict[str, Any]:
    hours = Counter()
    weekdays = Counter()
    total_posts = 0
    weekend_posts = 0
    
    for p in posts:
        if p.timestamp:
            h = p.timestamp.hour
            wd = p.timestamp.weekday()
            hours[h] += 1
            weekdays[wd] += 1
            total_posts += 1
            if wd >= 5:  # Saturday=5, Sunday=6
                weekend_posts += 1
                
    weekend_ratio = weekend_posts / total_posts if total_posts > 0 else 0.0
    
    # Activity window (densest 8-hour window)
    activity_window = {'start_hour': 0, 'end_hour': 7, 'peak_hour': 0}
    if hours:
        max_density = -1
        best_start = 0
        for start_h in range(24):
            # sum counts in window [start_h, (start_h+7)%24]
            window_sum = sum(hours[(start_h + i) % 24] for i in range(8))
            if window_sum > max_density:
                max_density = window_sum
                best_start = start_h
        
        # peak hour in the best window
        best_end = (best_start + 7) % 24
        window_hours_counts = { (best_start + i) % 24: hours[(best_start + i) % 24] for i in range(8) }
        peak_h = max(window_hours_counts, key=window_hours_counts.get)
        
        activity_window = {'start_hour': best_start, 'end_hour': best_end, 'peak_hour': peak_h}
        
    # Timezone consistency (Shannon entropy of hour distribution)
    timezone_consistency = 0.0
    if total_posts > 0:
        entropy = 0.0
        for count in hours.values():
            if count > 0:
                p_i = count / total_posts
                entropy -= p_i * math.log2(p_i)
        
        # Max entropy for 24 bins is log2(24) ~ 4.58
        max_entropy = math.log2(24)
        if max_entropy > 0:
            # normalized entropy 0 to 1
            normalized_entropy = entropy / max_entropy
            # high consistency = low entropy
            timezone_consistency = 1.0 - normalized_entropy
    
    return {
        "posting_hours": dict(hours),
        "weekday_distribution": dict(weekdays),
        "activity_window": activity_window,
        "weekend_ratio": weekend_ratio,
        "timezone_consistency": timezone_consistency
    }
