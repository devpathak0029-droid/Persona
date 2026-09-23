from pydantic import BaseModel, Field

class CorpusQuality(BaseModel):
    posts: int
    clean_characters: int
    language: str | None
    eligible: bool
    reasons: list[str] = Field(default_factory=list)

class Corpus(BaseModel):
    corpus_id: str
    posts: list
    quality: CorpusQuality | None = None
    corpus_hash: str | None = None
