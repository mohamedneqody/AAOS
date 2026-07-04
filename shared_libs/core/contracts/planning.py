from pydantic import BaseModel, ConfigDict
from typing import List

class LogicalPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: str = "1.0"
    capabilities: List[str]
    confidence: float
