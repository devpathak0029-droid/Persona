try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

import numpy as np

# We load a small, fast embedding model suitable for semantic similarity.
# In a full deployment, this can be swapped for a larger model like RoBERTa or an LLM embedding API.
_model = None

def get_model(model_name: str = 'all-MiniLM-L6-v2'):
    global _model
    if _model is None and SentenceTransformer is not None:
        try:
            _model = SentenceTransformer(model_name)
        except Exception as e:
            print(f"Failed to load sentence-transformers model {model_name}: {e}")
    return _model

def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """Generates dense vector embeddings for a list of texts."""
    model = get_model()
    if not model or not texts:
        return []
    
    # Generate embeddings and convert to standard python floats for JSON serialization
    try:
        embeddings = model.encode(texts)
        return [vec.tolist() for vec in embeddings]
    except Exception as e:
        print(f"Failed to encode texts: {e}")
        return []

def centroid(embeddings: list[list[float]]) -> list[float]:
    """Calculates the centroid (average) embedding for a list of embeddings."""
    if not embeddings:
        return []
    return np.mean(embeddings, axis=0).tolist()

def average_embedding(embeddings: list[list[float]]) -> list[float]:
    """Alias for centroid, calculates the average embedding."""
    return centroid(embeddings)
