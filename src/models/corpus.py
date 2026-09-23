from pydantic import BaseModel, Field

class CorpusQuality(BaseModel):
    post_count: int
    character_count: int
    eligible: bool
    reasons: list[str] = Field(default_factory=list)
    duplicates_removed: int
    templates_removed: int
    contamination_detected: bool
    language: str | None
    corpus_hash: str

class Corpus(BaseModel):
    corpus_id: str
    posts: list
    quality: CorpusQuality | None = None
    corpus_hash: str | None = None
