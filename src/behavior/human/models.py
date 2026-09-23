import uuid
from typing import List, Literal, TypedDict
from pydantic import BaseModel, Field

class HumanBehaviorSignal(BaseModel):
    """
    PRALAYX Human-Behavior Signal Model.
    Captures observable linguistic and operational characteristics without assigning identity.
    """
    signal_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    category: Literal['identity', 'communication', 'temporal', 'platform', 'operational']
    signal_type: str
    observations: List[str]
    evidence_ids: List[str]
    confidence: float = Field(ge=0.0, le=1.0)
    explanation: str
    limitations: List[str]
