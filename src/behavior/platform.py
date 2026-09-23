from collections import Counter
from typing import Dict, Any

def platform_activity(posts: list) -> Dict[str, Any]:
    """Analyze cross-platform behavior."""
    platforms = Counter()
    timeline = {}
    
    for p in posts:
        plat = getattr(p, 'platform', None) or "unknown"
        platforms[plat] += 1
        
        if plat not in timeline:
            timeline[plat] = {'first_seen': None, 'last_seen': None, 'post_count': 0}
            
        timeline[plat]['post_count'] += 1
        
        if getattr(p, 'timestamp', None):
            ts = p.timestamp
            curr_first = timeline[plat]['first_seen']
            curr_last = timeline[plat]['last_seen']
            
            if curr_first is None or ts < curr_first:
                timeline[plat]['first_seen'] = ts
            if curr_last is None or ts > curr_last:
                timeline[plat]['last_seen'] = ts
                
    # Convert datetimes to ISO strings for timeline output
    for plat in timeline:
        if timeline[plat]['first_seen']:
            timeline[plat]['first_seen'] = timeline[plat]['first_seen'].isoformat()
        if timeline[plat]['last_seen']:
            timeline[plat]['last_seen'] = timeline[plat]['last_seen'].isoformat()

    primary_platform = platforms.most_common(1)[0][0] if platforms else None
    
    return {
        'platforms': dict(platforms),
        'primary_platform': primary_platform,
        'platform_count': len(platforms),
        'cross_platform': len(platforms) > 1,
        'platform_timeline': timeline
    }
