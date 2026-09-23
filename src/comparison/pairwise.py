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
            
    # Topic similarity
    from src.semantic.topics import topic_overlap
    topics_a = profile_a.get('semantic', {}).get('topics', {})
    topics_b = profile_b.get('semantic', {}).get('topics', {})
    topic_overlap_res = topic_overlap(topics_a, topics_b)
    topic_sim = topic_overlap_res.get('topic_similarity', 0.0)
            
    # Behavior association
    beh_a = profile_a.get('behavior', {}).get('temporal', {}).get('posting_hours', {})
    beh_b = profile_b.get('behavior', {}).get('temporal', {}).get('posting_hours', {})
    beh_sim = vector_similarity(beh_a, beh_b) if beh_a and beh_b else 0.0
    
    # Temporal association
    temp_a = profile_a.get('behavior', {}).get('temporal', {})
    temp_b = profile_b.get('behavior', {}).get('temporal', {})
    temporal_sim = 0.0
    if temp_a and temp_b:
        hours_a = set(temp_a.get('posting_hours', {}).keys())
        hours_b = set(temp_b.get('posting_hours', {}).keys())
        if hours_a and hours_b:
            shared = hours_a.intersection(hours_b)
            union = hours_a.union(hours_b)
            temporal_sim = float(len(shared) / len(union)) if union else 0.0
    
    return {
        'persona_a': profile_a.get('persona_id', 'A'),
        'persona_b': profile_b.get('persona_id', 'B'),
        'style_similarity': style_sim,
        'semantic_similarity': semantic_sim,
        'topic_similarity': topic_sim,
        'behavioral_association': beh_sim,
        'temporal_association': temporal_sim,
        'explanation': 'Comparison based on observable analytical characteristics. Shows temporal overlap, not timezone proof.',
        'evidence_ids': [],
        'limitations': ['Associations represent hypotheses, not identity proof.', 'Temporal overlap does not definitively prove same timezone.'],
        'analysis_version': '3.0.0'
    }
