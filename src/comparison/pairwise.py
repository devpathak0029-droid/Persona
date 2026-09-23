import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def vector_similarity(a: dict, b: dict) -> float:
    keys = sorted(set(a) | set(b))
    va = np.array([float(a.get(k, 0)) for k in keys]).reshape(1, -1)
    vb = np.array([float(b.get(k, 0)) for k in keys]).reshape(1, -1)
    if not np.any(va) or not np.any(vb):
        return 0.0
    return float(cosine_similarity(va, vb)[0][0])
