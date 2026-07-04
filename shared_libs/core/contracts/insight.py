from pydantic import BaseModel, ConfigDict
from typing import List, Any

class InsightPackage(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: str = "1.0"
    insights: List[str]
    metrics: dict[str, Any]
