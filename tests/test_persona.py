import pytest
from src.persona.evolution import analyze_evolution
from src.preprocessing.corpus_quality import assess_quality
from src.fusion.engine import fuse_signals
from src.comparison.pairwise import compare_profiles
from src.comparison.ranking import rank_candidates

class DummyPost:
    def __init__(self, text, ts):
        self.text = text
        self.timestamp = ts

def test_question_ratio_evolution():
    posts = [DummyPost("Text?", f"2026-01-0{i}") for i in range(1, 10)]
    
    def mock_stylometry(text):
        return {'sentence_structure': {'question_ratio': 0.5}}
        
    result = analyze_evolution(posts, stylometry_fn=mock_stylometry)
    assert 'changes' in result
    question_changes = [c for c in result['changes'] if c['feature'] == 'question_ratio']
    assert len(question_changes) == 1
    assert question_changes[0]['early'] == 0.5

def test_corpus_eligibility():
    eligible_posts = [DummyPost("test", "ts") for _ in range(5)]
    cleaned_texts = ["test" * 150 for _ in range(5)] # length > 500
    res = assess_quality(eligible_posts, cleaned_texts, "en", 0.1)
    assert res['eligible'] is True

    ineligible_posts = [DummyPost("test", "ts") for _ in range(2)]
    res2 = assess_quality(ineligible_posts, ["test", "test"], "en", 0.1)
    assert res2['eligible'] is False

def test_fusion():
    signals = {
        'style_similarity': 0.8,
        'semantic_similarity': 0.7,
        'behavioral_association': 0.9,
        'topic_similarity': 0.5,
        'temporal_association': 0.6
    }
    res = fuse_signals(signals)
    assert 'combined_confidence' in res
    assert 'confidence_band' in res
    assert 'explanation' in res
    assert res['combined_confidence'] > 0.6
    assert 'limitations' in res

def test_pairwise_comparison_with_fusion():
    prof_a = {'persona_id': 'A'}
    prof_b = {'persona_id': 'B'}
    comp = compare_profiles(prof_a, prof_b)
    assert 'fusion' in comp
    assert 'combined_confidence' in comp['fusion']

def test_ranking_uses_fusion():
    target = {'persona_id': 'T'}
    c1 = {'persona_id': 'C1'}
    c2 = {'persona_id': 'C2'}
    
    # Mocking is a bit tricky without patching, but since compare_profiles will return 0 for empty profiles,
    # let's just make sure it returns a list of dictionaries with 'weighted_score'.
    res = rank_candidates(target, [c1, c2])
    assert len(res) == 2
    assert 'weighted_score' in res[0]
    assert 'note' in res[0]

def test_empty_weak_signals():
    signals = {
        'style_similarity': 0.1,
        'semantic_similarity': 0.1,
        'behavioral_association': 0.1,
        'topic_similarity': 0.1,
        'temporal_association': 0.1
    }
    res = fuse_signals(signals)
    assert res['confidence_band'] == 'LOW'
    assert len(res['limitations']) > 2 # Should include warnings about weak signals
