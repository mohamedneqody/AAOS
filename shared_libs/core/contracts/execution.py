from pydantic import BaseModel, ConfigDict, Field
from typing import List, Dict, Any, Optional
from enum import Enum

class ExecutionState(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"
    SKIPPED = "SKIPPED"
    TIMEOUT = "TIMEOUT"
    CANCELLED = "CANCELLED"
    RETRYING = "RETRYING"

class Manifest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    worker: str
    worker_class: str = Field(alias="class")
    version: str
    timeout: int
    retry: bool
    estimated_cost: float
    estimated_duration: float
    entry_point: str

class Evidence(BaseModel):
    model_config = ConfigDict(extra="forbid")
    evidence_id: str
    execution_id: str
    graph_id: str
    worker: str
    worker_version: str
    tool: str
    tool_version: str
    capability: str
    source: str
    timestamp: str
    confidence: float
    hash: str
    checksum: str
    metadata: Dict[str, Any]
    version: str = "1.0"

class PluginResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: str = "1.0"
    plugin: str
    worker: str
    worker_version: str
    capability: str
    status: str
    started_at: str
    finished_at: str
    duration_ms: float
    confidence: float
    metadata: Dict[str, Any]
    evidence: List[Evidence]

class ExecutionResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: str = "1.0"
    execution_id: str
    graph_id: str
    status: str
    started_at: str
    finished_at: str
    duration_ms: float
    plugin_results: List[PluginResult]
    evidence: List[Evidence]
    execution_metadata: Dict[str, Any]

class ExecutionNode(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    version: str = "1.0"
    capability: str
    tool: str
    worker: str
    manifest_version: str = "1.0"
    dependencies: List[str]
    parallel_group: str
    estimated_cost: float
    estimated_duration: float
    retryable: bool
    timeout_seconds: int
    priority: int
    status: str
    parameters: Dict[str, Any] = Field(default_factory=dict)

class ExecutionGraph(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: str = "1.0"
    graph_id: str
    graph_version: str = "1.0"
    created_at: str
    planner_version: str
    execution_mode: str
    nodes: List[ExecutionNode]
    edges: List[dict]

