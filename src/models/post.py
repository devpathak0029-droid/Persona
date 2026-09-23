from pydantic import BaseModel, Field
from datetime import datetime

class Post(BaseModel):
    post_id: str
    author_id: str | None = None
    platform: str
    text: str
    timestamp: datetime | None = None
    source_url: str | None = None
    metadata: dict = Field(default_factory=dict)
