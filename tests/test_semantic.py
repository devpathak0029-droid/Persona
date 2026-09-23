import pytest
import numpy as np
from unittest.mock import patch, MagicMock

from src.semantic.embeddings import generate_embeddings, centroid, average_embedding
from src.semantic.similarity import semantic_similarity
from src.semantic.topics import extract_topics, topic_overlap

class MockModel:
    def encode(self, texts):
        # Return dummy embeddings (dim=3) for testing
        return np.array([[1.0, 0.0, 0.0] for _ in texts])

def test_embeddings():
    with patch('src.semantic.embeddings.get_model', return_value=MockModel()):
        texts = ["hello", "world"]
        embeddings = generate_embeddings(texts)
        assert len(embeddings) == 2
        assert len(embeddings[0]) == 3
        assert embeddings[0] == [1.0, 0.0, 0.0]

def test_centroid():
    embeddings = [
        [1.0, 2.0, 3.0],
        [3.0, 4.0, 5.0]
    ]
    cent = centroid(embeddings)
    assert cent == [2.0, 3.0, 4.0]
    
    avg = average_embedding(embeddings)
    assert avg == cent

def test_semantic_similarity():
    emb_a = [[1.0, 0.0, 0.0], [1.0, 0.0, 0.0]]
    emb_b = [[0.0, 1.0, 0.0], [0.0, 1.0, 0.0]]
    # orthogonal vectors, cosine similarity should be 0
    res = semantic_similarity(emb_a, emb_b)
    assert res['centroid_similarity'] == 0.0
    assert res['max_pairwise_similarity'] == 0.0
    
    emb_c = [[1.0, 0.0, 0.0]]
    res2 = semantic_similarity(emb_a, emb_c)
    assert res2['centroid_similarity'] > 0.99
    assert res2['max_pairwise_similarity'] > 0.99

def test_extract_topics():
    texts = [
        "python programming language",
        "python coding tutorial",
        "java programming language",
        "c++ coding tutorial"
    ]
    res = extract_topics(texts, n_topics=2, top_words_per_topic=2)
    assert res["n_topics_found"] == 2
    assert len(res["topics"]) == 2
    assert "weight" in res["topics"][0]
    
    # Test insufficient texts
    res2 = extract_topics(["python"], n_topics=2)
    assert res2["n_topics_found"] == 0

def test_topic_overlap():
    topics_a = {
        'topics': [
            {'top_words': ['python', 'programming']},
            {'top_words': ['coding', 'tutorial']}
        ]
    }
    topics_b = {
        'topics': [
            {'top_words': ['python', 'java']},
            {'top_words': ['scripting', 'tutorial']}
        ]
    }
    res = topic_overlap(topics_a, topics_b)
    # words_a: python, programming, coding, tutorial
    # words_b: python, java, scripting, tutorial
    # shared: python, tutorial (2)
    # total unique: python, programming, coding, tutorial, java, scripting (6)
    # jaccard = 2 / 6 = 0.333...
    assert "python" in res["shared_terms"]
    assert "tutorial" in res["shared_terms"]
    assert abs(res["topic_similarity"] - 0.3333) < 0.01
    assert "programming" in res["unique_to_a"]
    assert "java" in res["unique_to_b"]
