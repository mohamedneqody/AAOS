from pydantic import BaseModel, ConfigDict
from typing import List, Any

from .dataset import DatasetProfile
from .semantic import SemanticModel
from .planning import LogicalPlan
from .policy import PolicyDecision
from .execution import ExecutionGraph

class PlanningArtifact(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: str = "1.0"
    dataset_profile: DatasetProfile
    semantic_model: SemanticModel
    logical_plan: LogicalPlan
    policy_decision: PolicyDecision
    execution_graph: ExecutionGraph
    metadata: dict
    request_id: str
    session_id: str
    planner_model: str
    runtime_version: str
    planning_duration_ms: int
    artifact_version: str
    timestamp: str
    overall_confidence: float
