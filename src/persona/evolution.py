from datetime import datetime
from typing import List, Dict, Any

def analyze_evolution(posts: List[Any], stylometry_fn=None) -> Dict[str, Any]:
    """
    Analyze how a persona's writing style evolves over time.
    """
    if len(posts) < 6:
        return {'status': 'insufficient_data'}
    
    if stylometry_fn is None:
        from ..stylometry.engine import analyze_style
        stylometry_fn = analyze_style
        
    # Sort posts by timestamp. Assuming posts have a 'timestamp' attribute or key.
    # Posts are Pydantic models but could be dicts, handle both.
    def get_ts(p):
        return p.timestamp if hasattr(p, 'timestamp') else p.get('timestamp')
        
    def get_text(p):
        return p.text if hasattr(p, 'text') else p.get('text', '')
    
    sorted_posts = sorted([p for p in posts if get_ts(p)], key=get_ts)
    if len(sorted_posts) < 6:
         return {'status': 'insufficient_data'}
         
    n = len(sorted_posts)
    third = n // 3
    early_posts = sorted_posts[:third]
    middle_posts = sorted_posts[third:2*third]
    late_posts = sorted_posts[-third:]
    
    def combine_and_analyze(period_posts):
        text = "\n".join(get_text(p) for p in period_posts)
        if not text.strip():
            return {}
        return stylometry_fn(text)
        
    early_stats = combine_and_analyze(early_posts)
    middle_stats = combine_and_analyze(middle_posts)
    late_stats = combine_and_analyze(late_posts)
    
    periods = []
    for name, p_posts, p_stats in [('early', early_posts, early_stats), 
                                   ('middle', middle_posts, middle_stats), 
                                   ('late', late_posts, late_stats)]:
        periods.append({
            'name': name,
            'start': get_ts(p_posts[0]) if p_posts else None,
            'end': get_ts(p_posts[-1]) if p_posts else None,
            'post_count': len(p_posts),
            'stylometry_summary': p_stats
        })
        
    # Compare early vs late on key metrics
    # avg_word_length, type_token_ratio, mean_sentence_length, question_ratio
    metrics = {
        'avg_word_length': ('lexical', 'avg_word_length'),
        'type_token_ratio': ('lexical', 'type_token_ratio'),
        'mean_sentence_length': ('sentence_structure', 'mean_length'),
        'question_ratio': ('punctuation', 'question_ratio') # examples
    }
    
    def get_metric(stats, cat, key):
        if not stats: return None
        return stats.get(cat, {}).get(key)
        
    changes = []
    stable_features = []
    drift_features = []
    total_drift = 0.0
    valid_metrics = 0
    
    for metric_name, (cat, key) in metrics.items():
        early_val = get_metric(early_stats, cat, key)
        late_val = get_metric(late_stats, cat, key)
        
        if early_val is not None and late_val is not None and early_val != 0:
            drift = abs(late_val - early_val) / abs(early_val)
            # normalized drift roughly
            drift_val = drift
        elif early_val == 0 and late_val != 0:
            drift_val = 1.0 # arbitrary large drift
        elif early_val == 0 and late_val == 0:
            drift_val = 0.0
        else:
            continue
            
        changes.append({
            'feature': metric_name,
            'early_value': early_val,
            'late_value': late_val,
            'drift': drift_val
        })
        
        if drift_val < 0.10:
            stable_features.append(metric_name)
        if drift_val > 0.25:
            drift_features.append(metric_name)
            
        total_drift += min(drift_val, 1.0)
        valid_metrics += 1
        
    overall_drift_score = (total_drift / valid_metrics) if valid_metrics > 0 else 0.0
    
    return {
        'periods': periods,
        'changes': changes,
        'stable_features': stable_features,
        'drift_features': drift_features,
        'overall_drift_score': overall_drift_score
    }
