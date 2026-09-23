from typing import Dict, Any

def _get_period_stats(stamps: list) -> Dict[str, Any]:
    if not stamps:
        return {'start': None, 'end': None, 'post_count': 0, 'posts_per_day': 0.0}
    
    start_time = stamps[0]
    end_time = stamps[-1]
    duration_days = max((end_time - start_time).total_seconds() / 86400, 1.0)
    
    return {
        'start': start_time.isoformat(),
        'end': end_time.isoformat(),
        'post_count': len(stamps),
        'posts_per_day': len(stamps) / duration_days
    }

def analyze_lifecycle(posts: list) -> Dict[str, Any]:
    """Determine lifecycle stage of the persona."""
    stamps = sorted(p.timestamp for p in posts if p.timestamp)
    
    if len(stamps) < 3:
        return {
            'stage': 'insufficient_data',
            'periods': {
                'early': _get_period_stats([]),
                'middle': _get_period_stats([]),
                'late': _get_period_stats([])
            },
            'trend': 'unknown'
        }
        
    n = len(stamps)
    third = n // 3
    
    # If not perfectly divisible, put remainder in late
    early_stamps = stamps[:third]
    middle_stamps = stamps[third:2*third]
    late_stamps = stamps[2*third:]
    
    early_stats = _get_period_stats(early_stamps)
    middle_stats = _get_period_stats(middle_stamps)
    late_stats = _get_period_stats(late_stamps)
    
    # Simple trend logic based on posts_per_day
    e_rate = early_stats['posts_per_day']
    m_rate = middle_stats['posts_per_day']
    l_rate = late_stats['posts_per_day']
    
    if l_rate > m_rate and m_rate >= e_rate:
        trend = 'increasing'
    elif l_rate < m_rate and m_rate <= e_rate:
        trend = 'decreasing'
    elif abs(l_rate - e_rate) < 0.1 * (e_rate if e_rate > 0 else 1.0):
        trend = 'stable'
    else:
        trend = 'unknown'
        
    # Determine stage
    if l_rate == 0 and m_rate == 0:
        stage = 'dormant'
    elif trend == 'increasing' or (l_rate > 0 and e_rate == 0):
        stage = 'emerging'
    elif trend == 'decreasing':
        stage = 'declining'
    elif l_rate > 0:
        stage = 'active'
    else:
        stage = 'insufficient_data'
        
    return {
        'stage': stage,
        'periods': {
            'early': early_stats,
            'middle': middle_stats,
            'late': late_stats
        },
        'trend': trend
    }
