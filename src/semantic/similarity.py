import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .embeddings import centroid

def semantic_similarity(embeddings_a: list[list[float]], embeddings_b: list[list[float]], method: str = 'cosine') -> dict:
    """
    Computes semantic similarity between two sets of embeddings.
    """
    if not embeddings_a or not embeddings_b:
        return {
            'semantic_similarity': 0.0,
            'method': method,
            'model': 'unknown',
            'centroid_similarity': 0.0,
            'max_pairwise_similarity': 0.0,
            'min_pairwise_similarity': 0.0,
            'mean_pairwise_similarity': 0.0,
            'explanation': 'One or both input embedding lists are empty.'
        }
    
    # Calculate centroids
    centroid_a = centroid(embeddings_a)
    centroid_b = centroid(embeddings_b)
    
    # Calculate centroid similarity
    try:
        cent_sim = cosine_similarity([centroid_a], [centroid_b])[0][0]
    except Exception:
        cent_sim = 0.0
    
    # Calculate pairwise similarities
    try:
        pairwise_sim = cosine_similarity(embeddings_a, embeddings_b)
        max_sim = float(np.max(pairwise_sim))
        min_sim = float(np.min(pairwise_sim))
        mean_sim = float(np.mean(pairwise_sim))
    except Exception:
        max_sim = 0.0
        min_sim = 0.0
        mean_sim = 0.0
    
    cent_sim = float(cent_sim)
    
    explanation = (
        f"Centroid cosine similarity is {cent_sim:.4f}. "
        f"The average pairwise similarity between sentences is {mean_sim:.4f}. "
        f"The highest similarity between any two sentences is {max_sim:.4f}."
    )
    
    return {
        'semantic_similarity': cent_sim,
        'method': method,
        'model': 'unknown',
        'centroid_similarity': cent_sim,
        'max_pairwise_similarity': max_sim,
        'min_pairwise_similarity': min_sim,
        'mean_pairwise_similarity': mean_sim,
        'explanation': explanation
    }
