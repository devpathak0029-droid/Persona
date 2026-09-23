from pydantic import BaseModel, Field

class ComparisonResult(BaseModel):
    persona_a: str
    persona_b: str
    style_similarity: float = 0.0
    semantic_similarity: float = 0.0
    topic_similarity: float = 0.0
    behavioral_association: float = 0.0
    temporal_association: float = 0.0
    explanation: str = ''
    evidence_ids: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    analysis_version: str = '3.0.0'
