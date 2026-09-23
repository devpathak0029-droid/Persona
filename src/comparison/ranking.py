from typing import List, Dict, Any

def rank_candidates(target_profile: Dict[str, Any], candidate_profiles: List[Dict[str, Any]], weights: Dict[str, float] = None) -> List[Dict[str, Any]]:
    """
    Rank candidate personas by analytical similarity to a target.
    """
    from .pairwise import compare_profiles
    
    if weights is None:
        weights = {
            'style': 0.35,
            'semantic': 0.25,
            'behavioral': 0.2,
            'topic': 0.1,
            'temporal': 0.1
        }
        
    results = []
    for cand in candidate_profiles:
        comp = compare_profiles(target_profile, cand)
        
        fusion = comp.get('fusion', {})
        weighted_score = fusion.get('combined_confidence', 0.0)
        signals = fusion.get('signals', {})
        
        results.append({
            'persona_id': cand.get('persona_id', 'unknown'),
            'weighted_score': weighted_score,
            'signals': signals
        })
        
    # Sort descending by weighted score
    results.sort(key=lambda x: x['weighted_score'], reverse=True)
    
    # Assign ranks and note
    for i, res in enumerate(results):
        res['rank'] = i + 1
        res['note'] = 'Ranked by analytical similarity. This is NOT identity attribution.'
        
    return results
