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
        
        signals = {
            'style_similarity': comp['style_similarity'],
            'semantic_similarity': comp['semantic_similarity'],
            'topic_similarity': comp['topic_similarity'],
            'behavioral_association': comp['behavioral_association'],
            'temporal_association': comp['temporal_association']
        }
        
        weighted_score = (
            signals['style_similarity'] * weights.get('style', 0.35) +
            signals['semantic_similarity'] * weights.get('semantic', 0.25) +
            signals['behavioral_association'] * weights.get('behavioral', 0.2) +
            signals['topic_similarity'] * weights.get('topic', 0.1) +
            signals['temporal_association'] * weights.get('temporal', 0.1)
        )
        
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
