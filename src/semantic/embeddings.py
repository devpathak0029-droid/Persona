from sentence_transformers import SentenceTransformer
import numpy as np

# We load a small, fast embedding model suitable for semantic similarity.
# In a full deployment, this can be swapped for a larger model like RoBERTa or an LLM embedding API.
_model = None

def get_model():
    global _model
    if _model is None:
        try:
            _model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            print(f"Failed to load sentence-transformers: {e}")
    return _model

def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """Generates dense vector embeddings for a list of texts."""
    model = get_model()
    if not model or not texts:
        return []
    
    # Generate embeddings and convert to standard python floats for JSON serialization
    embeddings = model.encode(texts)
    return [vec.tolist() for vec in embeddings]

def average_embedding(embeddings: list[list[float]]) -> list[float]:
    """Calculates the centroid (average) embedding for an actor's corpus."""
    if not embeddings:
        return []
    return np.mean(embeddings, axis=0).tolist()
