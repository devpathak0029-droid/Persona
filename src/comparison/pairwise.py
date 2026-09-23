import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def vector_similarity(a: dict, b: dict) -> float:
    keys = sorted(set(a) | set(b))
    va = np.array([float(a.get(k, 0)) for k in keys]).reshape(1, -1)
    vb = np.array([float(b.get(k, 0)) for k in keys]).reshape(1, -1)
    if not np.any(va) or not np.any(vb):
        return 0.0
    return float(cosine_similarity(va, vb)[0][0])

def compare_profiles(profile_a: dict, profile_b: dict) -> dict:
    # Style similarity
    style_a = profile_a.get('stylometry', {}).get('function_words', {})
    style_b = profile_b.get('stylometry', {}).get('function_words', {})
    style_sim = vector_similarity(style_a, style_b) if style_a and style_b else 0.0
    
    # Semantic similarity
    sem_a = profile_a.get('semantic', {}).get('centroid_embedding', [])
    sem_b = profile_b.get('semantic', {}).get('centroid_embedding', [])
    semantic_sim = 0.0
    if sem_a and sem_b:
        va = np.array(sem_a).reshape(1, -1)
        vb = np.array(sem_b).reshape(1, -1)
        if np.any(va) and np.any(vb):
            semantic_sim = float(cosine_similarity(va, vb)[0][0])
            
    # Behavior association
    beh_a = profile_a.get('behavior', {}).get('temporal', {}).get('posting_hours', {})
    beh_b = profile_b.get('behavior', {}).get('temporal', {}).get('posting_hours', {})
    beh_sim = vector_similarity(beh_a, beh_b) if beh_a and beh_b else 0.0
    
    return {
        'persona_a': profile_a.get('persona_id', 'A'),
        'persona_b': profile_b.get('persona_id', 'B'),
        'style_similarity': style_sim,
        'semantic_similarity': semantic_sim,
        'topic_similarity': 0.0,
        'behavioral_association': beh_sim,
        'temporal_association': 0.0,
        'explanation': 'Comparison based on observable analytical characteristics.',
        'evidence_ids': [],
        'limitations': ['Associations represent hypotheses, not identity proof.'],
        'analysis_version': '3.0.0'
    }
