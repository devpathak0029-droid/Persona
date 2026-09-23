from pydantic import BaseModel, Field
from datetime import datetime, timezone

def utc_now():
    return datetime.now(timezone.utc)

class Evidence(BaseModel):
    evidence_id: str
    category: str
    source: str
    source_url: str | None = None
    post_ids: list[str] = Field(default_factory=list)
    feature: str = ''
    observation: str = ''
    explanation: str
    confidence: float = Field(ge=0, le=1)
    analysis_version: str = '3.0.0'
    corpus_hash: str = ''
    created_at: datetime = Field(default_factory=utc_now)
    captured_at: datetime = Field(default_factory=utc_now)
    original_timestamps: list[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)
