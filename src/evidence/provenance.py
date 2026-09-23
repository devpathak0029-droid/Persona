import uuid
import datetime
from typing import Dict, Any, List, Optional

def generate_evidence_id() -> str:
    """Generate a unique evidence ID."""
    return f"EVD-{uuid.uuid4().hex[:12]}"

def create_evidence(
    category: str,
    feature: str,
    observation: str,
    explanation: str,
    confidence: float,
    source: str = 'persona-analysis',
    post_ids: Optional[List[str]] = None,
    corpus_hash: str = ''
) -> Dict[str, Any]:
    """
    Create a complete evidence dictionary with all required fields.
    """
    return {
        'evidence_id': generate_evidence_id(),
        'category': category,
        'source': source,
        'source_url': '',
        'post_ids': post_ids or [],
        'feature': feature,
        'observation': observation,
        'explanation': explanation,
        'confidence': confidence,
        'analysis_version': '3.0.0',
        'corpus_hash': corpus_hash,
        'captured_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'original_timestamps': [],
        'metadata': {}
    }
