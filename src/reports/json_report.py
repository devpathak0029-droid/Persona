import datetime
from typing import Dict, Any, Optional

def generate_json_report(
    profile: Dict[str, Any], 
    comparison: Optional[Dict[str, Any]] = None, 
    fusion: Optional[Dict[str, Any]] = None, 
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Generate the full JSON report structure.
    """
    corpus_quality = profile.get('corpus_quality', {})
    post_count = corpus_quality.get('post_count', 0)
    is_eligible = corpus_quality.get('eligible', post_count >= 5)
    evidence_count = len(profile.get('evidence', []))
    
    exec_summary = (
        f"This report presents the persona analysis based on a corpus of {post_count} posts. "
        f"The corpus was {'eligible' if is_eligible else 'not eligible'} for reliable stylometric analysis. "
        f"A total of {evidence_count} key findings were identified across behavioral, semantic, and linguistic vectors."
    )
    
    return {
        'report_version': '3.0.0',
        'generated_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'metadata': metadata or {},
        'executive_summary': exec_summary,
        'corpus_quality': corpus_quality,
        'linguistic_fingerprint': profile.get('stylometry'),
        'semantic_profile': profile.get('semantic'),
        'behavioral_profile': profile.get('behavior'),
        'persona_evolution': profile.get('evolution'),
        'migration_hypotheses': profile.get('migration'),
        'cross_persona_comparison': comparison,
        'evidence_ledger': profile.get('evidence', []),
        'confidence': fusion,
        'limitations': profile.get('limitations', [])
    }
