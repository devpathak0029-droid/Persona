from pydantic import BaseModel, Field

class PersonaProfile(BaseModel):
    persona_id: str
    corpus_quality: dict
    stylometry: dict = Field(default_factory=dict)
    semantic: dict = Field(default_factory=dict)
    behavior: dict = Field(default_factory=dict)
    evolution: dict = Field(default_factory=dict)
    migration: dict = Field(default_factory=dict)
    evidence: list[dict] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    analysis_version: str = "1.0.0"
