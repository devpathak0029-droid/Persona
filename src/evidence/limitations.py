from typing import Dict, Any, List

def generate_limitations(
    corpus_quality: Dict[str, Any],
    has_ai: bool,
    has_embeddings: bool,
    comparison_count: int = 0
) -> List[str]:
    """
    Auto-generate limitations based on analysis conditions.
    """
    limitations = []
    
    post_count = corpus_quality.get('post_count', 0)
    duplicate_ratio = corpus_quality.get('duplicate_ratio', 0.0)
    
    if post_count < 5:
        limitations.append("Corpus below minimum threshold for reliable stylometric comparison")
    elif post_count < 10:
        limitations.append(f"Small corpus size ({post_count} posts) may reduce stylometric reliability")
        
    if duplicate_ratio > 0.3:
        limitations.append(f"High duplicate ratio ({duplicate_ratio * 100:.1f}%) may distort frequency-based features")
        
    if not has_ai:
        limitations.append("AI-based linguistic profiling was not available for this analysis")
        
    if not has_embeddings:
        limitations.append("Semantic embeddings could not be generated; semantic similarity unavailable")
        
    if comparison_count < 2:
        limitations.append("Single-profile analysis only; cross-persona comparison not performed")
        
    limitations.append("Stylometric similarity does not constitute proof of identity")
    limitations.append("Behavioral patterns are associative, not deterministic")
    
    return limitations
