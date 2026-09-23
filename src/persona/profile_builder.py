"""Main profile builder — orchestrates all analysis modules."""
from __future__ import annotations

from ..preprocessing.cleaner import clean_text, clean_post, corpus_hash
from ..preprocessing.language_detector import detect_language
from ..preprocessing.deduplicator import deduplicate
from ..preprocessing.corpus_quality import assess_quality
from ..preprocessing.template_detector import detect_templates
from ..preprocessing.identifier_filter import filter_identifiers
from ..stylometry.engine import analyze_style
from ..stylometry.ai_profiler import generate_ai_profile
from ..semantic.embeddings import generate_embeddings, centroid
from ..semantic.topics import extract_topics
from ..behavior.engine import analyze_behavior
from ..behavior.human.engine import analyze_human_behavior
from .evolution import analyze_evolution
from ..evidence.provenance import create_evidence
from ..evidence.limitations import generate_limitations


def build_profile(persona_id: str, posts: list, **kwargs) -> dict:
    """
    Build a complete persona profile from a list of Post objects.

    Accepts optional PRALAYX IDs via kwargs:
        investigation_id, actor_id, run_id, session_id
    """
    investigation_id = kwargs.get("investigation_id")
    actor_id = kwargs.get("actor_id")
    run_id = kwargs.get("run_id")
    session_id = kwargs.get("session_id")

    if not posts:
        return {
            "investigation_id": investigation_id,
            "actor_id": actor_id,
            "run_id": run_id,
            "session_id": session_id,
            "persona_id": persona_id,
            "corpus_quality": {"posts": 0, "clean_characters": 0, "language": None,
                               "duplicate_ratio": 0.0, "eligible": False,
                               "reasons": ["No posts provided."]},
            "stylometry": {
                "lexical": {}, "function_words": {}, "punctuation": {}, "sentence_structure": {},
                "character_ngrams": {}, "spelling": {}, "emoji": {}, "syntax": {}
            },
            "semantic": {
                "embedding_model": "all-MiniLM-L6-v2", "corpus_centroid": [], "semantic_similarity": None,
                "topics": {}, "topic_similarity": None
            },
            "behavior": {
                "temporal": {}, "frequency": {}, "bursts": {}, "inactive_periods": [],
                "lifecycle": {}, "platform_activity": {}
            },
            "human_behavior": {},
            "ai_profile": {},
            "evolution": {},
            "migration": {},
            "comparisons": [],
            "evidence": [],
            "confidence": {},
            "limitations": ["No posts provided for analysis."],
            "analysis_version": "4.0.0"
        }

    # ── Preprocessing ──────────────────────────────────────────────
    def get_text(p): return p.text if hasattr(p, 'text') else p.get('text', '')
    def get_id(p, i): return p.post_id if hasattr(p, 'post_id') else p.get('post_id', str(i))

    raw_texts = [get_text(p) for p in posts]
    cleaned = [clean_text(get_text(p)) for p in posts]
    combined = "\n".join(x for x in cleaned if x)

    # Deduplication
    post_dicts = [{"post_id": get_id(p, i), "text": get_text(p)}
                  for i, p in enumerate(posts)]
    dedup_result = deduplicate(post_dicts)
    duplicate_ratio = dedup_result.get("duplicate_ratio", 0.0)

    # Language detection
    lang = detect_language(combined)

    # Corpus quality assessment
    quality = assess_quality(posts, cleaned, lang, duplicate_ratio)
    eligible = quality.get("eligible", False)
    c_hash = corpus_hash(cleaned)

    # ── Evidence collection ────────────────────────────────────────
    evidence_items: list[dict] = []

    # ── Stylometry ─────────────────────────────────────────────────
    stylometry_data: dict = {
        "lexical": {}, "function_words": {}, "punctuation": {}, "sentence_structure": {},
        "character_ngrams": {}, "spelling": {}, "emoji": {}, "syntax": {}
    }
    ai_profile = {}
    if eligible:
        stylometry_data = analyze_style(combined)

        # AI-based linguistic profiling (optional, never blocks)
        ai_profile = generate_ai_profile(combined)
        if ai_profile.get("status") not in ("NOT_CONFIGURED", "ERROR"):
            evidence_items.append(create_evidence(
                category="AI_LINGUISTIC_PROFILE",
                feature="ai_analysis",
                observation="AI-generated observable linguistic characteristics",
                explanation="LLM analyzed communication style, formality, and recurring patterns.",
                confidence=0.6,
                corpus_hash=c_hash,
            ))

    # ── Semantic analysis ──────────────────────────────────────────
    has_embeddings = False
    semantic_data: dict = {
        "embedding_model": "all-MiniLM-L6-v2", 
        "corpus_centroid": [], 
        "semantic_similarity": None,
        "topics": {}, 
        "topic_similarity": None
    }
    if eligible:
        embeddings = generate_embeddings(cleaned)
        if embeddings:
            has_embeddings = True
            semantic_data["corpus_centroid"] = centroid(embeddings)

    # Topic analysis
    if eligible and len(cleaned) >= 3:
        semantic_data["topics"] = extract_topics(cleaned)

    # ── Behavioral analysis ────────────────────────────────────────
    behavior_data = {
        "temporal": {}, "frequency": {}, "bursts": {}, "inactive_periods": [],
        "lifecycle": {}, "platform_activity": {}
    }
    if eligible:
        behavior_data = analyze_behavior(posts)

    # ── Human Behavioral analysis ──────────────────────────────────
    human_behavior_data = {}
    if eligible:
        human_behavior_data = analyze_human_behavior(posts, cleaned)

    # ── Evolution analysis ─────────────────────────────────────────
    evolution_data: dict = {}
    if eligible:
        evolution_data = analyze_evolution(posts)

    # ── Limitations ────────────────────────────────────────────────
    limitations = generate_limitations(
        corpus_quality=quality,
        has_ai=ai_profile.get("status") not in ("NOT_CONFIGURED", "ERROR") if eligible else False,
        has_embeddings=has_embeddings,
        comparison_count=0,
    )

    # ── Assemble profile ───────────────────────────────────────────
    profile = {
        "investigation_id": investigation_id,
        "actor_id": actor_id,
        "run_id": run_id,
        "session_id": session_id,
        "persona_id": persona_id,
        "corpus_quality": quality,
        "stylometry": stylometry_data,
        "semantic": semantic_data,
        "behavior": behavior_data,
        "human_behavior": human_behavior_data,
        "ai_profile": ai_profile,
        "evolution": evolution_data,
        "migration": {},
        "comparisons": [],
        "evidence": evidence_items,
        "confidence": {},
        "limitations": limitations,
        "analysis_version": "4.0.0"
    }
    return profile
