from pydantic import BaseModel, ConfigDict
from typing import List
from .planning import LogicalPlan

class PolicyDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: str = "1.0"
    capabilities: LogicalPlan
    policy_passed: bool
    violations: List[str]
    decision_reason: str
