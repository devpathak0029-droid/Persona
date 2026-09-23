from ..preprocessing.cleaner import clean_text, corpus_hash
from ..preprocessing.language_detector import detect_language
from ..stylometry.engine import analyze_style
from ..stylometry.ai_profiler import generate_ai_profile
from ..semantic.embeddings import generate_embeddings, average_embedding
from ..behavior.engine import analyze_behavior

def build_profile(persona_id: str, posts: list) -> dict:
    cleaned = [clean_text(p.text) for p in posts]
    combined = "\n".join(x for x in cleaned if x)
    lang = detect_language(combined)
    eligible = len(posts) >= 5 and len(combined) >= 500
    
    # 1. Statistical Stylometry
    stylometry_data = analyze_style(combined) if eligible else {}
    
    # 2. AI-Based Semantic Profiling
    ai_profile = generate_ai_profile(combined) if eligible else {}
    if ai_profile and "error" not in ai_profile:
        stylometry_data["ai_analysis"] = ai_profile
        
    # 3. Dense Vector Embeddings (for cross-persona attribution matching)
    embeddings = generate_embeddings(cleaned) if eligible else []
    semantic_data = {
        "post_embeddings_count": len(embeddings),
        "centroid_embedding": average_embedding(embeddings)
    }
    
    profile = {
        "persona_id": persona_id,
        "corpus_quality": {
            "posts": len(posts),
            "clean_characters": len(combined),
            "language": lang,
            "eligible": eligible
        },
        "stylometry": stylometry_data,
        "semantic": semantic_data,
        "behavior": analyze_behavior(posts),
        "evolution": {},
        "migration": {},
        "evidence": [],
        "limitations": [] if eligible else ["Corpus below minimum quality threshold."],
        "analysis_version": "2.0.0-AI",
        "corpus_hash": corpus_hash(cleaned)
    }
    return profile
