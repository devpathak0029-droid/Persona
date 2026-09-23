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
    explanation: str
    confidence: float = Field(ge=0, le=1)
    created_at: datetime = Field(default_factory=utc_now)
    metadata: dict = Field(default_factory=dict)
