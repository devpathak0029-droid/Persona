from typing import Dict, Any, List

def detect_bursts(posts: list, gap_threshold_hours: float = 1.0) -> Dict[str, Any]:
    """Detect bursts of rapid posting activity."""
    stamps = sorted(p.timestamp for p in posts if p.timestamp)
    bursts = []
    
    if len(stamps) < 3:
        return {
            'bursts': [],
            'burst_count': 0,
            'posts_in_bursts': 0,
            'burst_ratio': 0.0
        }
        
    current_burst = [stamps[0]]
    
    for i in range(1, len(stamps)):
        gap = (stamps[i] - stamps[i-1]).total_seconds() / 3600
        if gap <= gap_threshold_hours:
            current_burst.append(stamps[i])
        else:
            if len(current_burst) >= 3:
                duration = (current_burst[-1] - current_burst[0]).total_seconds() / 3600
                bursts.append({
                    'start': current_burst[0].isoformat(),
                    'end': current_burst[-1].isoformat(),
                    'post_count': len(current_burst),
                    'duration_hours': duration
                })
            current_burst = [stamps[i]]
            
    # Check last burst
    if len(current_burst) >= 3:
        duration = (current_burst[-1] - current_burst[0]).total_seconds() / 3600
        bursts.append({
            'start': current_burst[0].isoformat(),
            'end': current_burst[-1].isoformat(),
            'post_count': len(current_burst),
            'duration_hours': duration
        })
        
    posts_in_bursts = sum(b['post_count'] for b in bursts)
    burst_ratio = posts_in_bursts / len(stamps) if len(stamps) > 0 else 0.0
    
    return {
        'bursts': bursts,
        'burst_count': len(bursts),
        'posts_in_bursts': posts_in_bursts,
        'burst_ratio': burst_ratio
    }

def detect_inactivity(posts: list, threshold_days: int = 7) -> List[Dict[str, Any]]:
    """Detect periods of inactivity longer than threshold_days."""
    stamps = sorted(p.timestamp for p in posts if p.timestamp)
    inactivity_periods = []
    
    if len(stamps) < 2:
        return inactivity_periods
        
    for i in range(1, len(stamps)):
        delta = stamps[i] - stamps[i-1]
        duration_days = delta.total_seconds() / 86400
        if duration_days > threshold_days:
            inactivity_periods.append({
                'start': stamps[i-1].isoformat(),
                'end': stamps[i].isoformat(),
                'duration_days': duration_days
            })
            
    return inactivity_periods
