from typing import List, Dict, Any

def build_similarity_matrix(profiles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Build a similarity matrix across multiple profiles.
    """
    from .pairwise import compare_profiles
    
    n = len(profiles)
    persona_ids = [p.get('persona_id', f'unknown_{i}') for i, p in enumerate(profiles)]
    
    style_matrix = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    semantic_matrix = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    behavior_matrix = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    
    pair_count = 0
    for i in range(n):
        for j in range(i + 1, n):
            res = compare_profiles(profiles[i], profiles[j])
            style_matrix[i][j] = style_matrix[j][i] = res['style_similarity']
            semantic_matrix[i][j] = semantic_matrix[j][i] = res['semantic_similarity']
            behavior_matrix[i][j] = behavior_matrix[j][i] = res['behavioral_association']
            pair_count += 1
            
    return {
        'persona_ids': persona_ids,
        'matrix': {
            'style': style_matrix,
            'semantic': semantic_matrix,
            'behavioral': behavior_matrix
        },
        'pair_count': pair_count
    }
