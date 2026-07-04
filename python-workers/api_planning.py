from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
import pandas as pd
import os
import yaml
import sys
import json
import uuid
import time
from datetime import datetime
from pydantic import BaseModel

sys.path.append("/app")
from shared_libs.ai_service.gemini import GeminiProvider
from shared_libs.core.exceptions import LLMValidationException, LLMException
from shared_libs.core.contracts import (
    DatasetProfile,
    SemanticModel,
    LogicalPlan,
    ExecutionNode,
    ExecutionGraph,
    PolicyDecision,
    PlanningArtifact
)

router = APIRouter(prefix="/api/planning", tags=["planning"])
llm = GeminiProvider()

# Global state to assemble the PlanningArtifact across sequential workflow nodes
_ARTIFACT_STATE = {}

class ProfilerRequest(BaseModel):
    file_path: str

class SemanticRequest(BaseModel):
    profile: DatasetProfile
    intent: str

class PlannerRequest(BaseModel):
    semantic_model: SemanticModel
    profile: DatasetProfile
    intent: str

class PolicyRequest(BaseModel):
    capabilities: LogicalPlan
    profile: DatasetProfile

class ExecutionPlannerRequest(BaseModel):
    capabilities: LogicalPlan

def load_yaml(path: str) -> dict:
    if os.path.exists(path):
        with open(path, "r") as f:
            return yaml.safe_load(f) or {}
    return {}

@router.post("/profiler", response_model=DatasetProfile)
def run_profiler(req: ProfilerRequest):
    if not os.path.exists(req.file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    df = pd.read_excel(req.file_path)
    
    sample_data = {}
    null_ratio = {}
    cardinality = {}
    candidate_measures = []
    candidate_dimensions = []
    candidate_time_columns = []
    business_keys = []
    
    row_count = len(df)
    duplicate_rows = int(df.duplicated().sum())
    duplicate_percentage = float(duplicate_rows / row_count) if row_count > 0 else 0.0
    
    for col in df.columns:
        vals = df[col].dropna().head(3).tolist()
        sample_data[col] = vals
        
        nulls = int(df[col].isnull().sum())
        null_ratio[col] = float(nulls / row_count) if row_count > 0 else 0.0
        
        card = int(df[col].nunique())
        cardinality[col] = card
        
        dtype = str(df[col].dtype)
        if "int" in dtype or "float" in dtype:
            candidate_measures.append(col)
        elif "object" in dtype or "bool" in dtype:
            candidate_dimensions.append(col)
        elif "datetime" in dtype:
            candidate_time_columns.append(col)
            
        if card == row_count and nulls == 0:
            business_keys.append(col)
            
    quality_score = float(max(0.0, 1.0 - (duplicate_percentage * 0.5) - (sum(null_ratio.values()) / max(1, len(df.columns)) * 0.5)))

    profile = DatasetProfile(
        dataset_name=os.path.basename(req.file_path),
        columns=df.columns.tolist(),
        row_count=row_count,
        column_count=len(df.columns),
        data_types={col: str(dtype) for col, dtype in df.dtypes.items()},
        missing_values=df.isnull().sum().to_dict(),
        duplicate_rows=duplicate_rows,
        duplicate_percentage=duplicate_percentage,
        candidate_measures=candidate_measures,
        candidate_dimensions=candidate_dimensions,
        candidate_time_columns=candidate_time_columns,
        business_keys=business_keys,
        cardinality=cardinality,
        null_ratio=null_ratio,
        quality_score=quality_score,
        sample_values=sample_data
    )
    _ARTIFACT_STATE['dataset_profile'] = profile
    return profile

@router.post("/semantic", response_model=SemanticModel)
def run_semantic(req: SemanticRequest):
    prompt = f"""
    You are a Data Semantic Analyzer.
    Analyze the following dataset profile and user intent to determine business entities, relationships, and the overall business meaning.
    
    User Intent: {req.intent}
    
    Dataset Profile:
    {req.profile.model_dump_json(indent=2)}
    """
    try:
        semantic_model = llm.generate_structured(
            prompt=prompt,
            response_model=SemanticModel
        )
        _ARTIFACT_STATE['semantic_model'] = semantic_model
        return semantic_model
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/planner", response_model=LogicalPlan)
def run_planner(req: PlannerRequest):
    caps_data = load_yaml("/app/registry/capabilities.yaml")
    routing_data = load_yaml("/app/registry/routing.yaml")
    
    available_caps = []
    if "capabilities" in caps_data:
        available_caps.extend(list(caps_data["capabilities"].keys()))
    if "routing" in routing_data:
        for cap in routing_data["routing"].keys():
            if cap not in available_caps:
                available_caps.append(cap)
                
    if not available_caps:
        available_caps = ["strategic_planning", "quality_review", "copy_generation", "analytics", "data_manipulation"]
        
    prompt = f"""
    You are a Planner Agent.
    Based on the semantic model, dataset profile, and user intent, choose the necessary capabilities from the Tool Registry.
    Do NOT output tool names, worker names, manifests, routing, or python modules. Only output the capabilities.
    
    User Intent: {req.intent}
    
    Semantic Model:
    {req.semantic_model.model_dump_json(indent=2)}
    
    Dataset Profile:
    {req.profile.model_dump_json(indent=2)}
    
    Available Capabilities:
    {json.dumps(available_caps, indent=2)}
    """
    
    try:
        logical_plan = llm.generate_structured(
            prompt=prompt,
            response_model=LogicalPlan
        )
        for cap in logical_plan.capabilities:
            if cap not in available_caps:
                raise HTTPException(status_code=500, detail=f"Layer 3 Validation Failed: Planner requested unknown capability '{cap}'")
                
        _ARTIFACT_STATE['logical_plan'] = logical_plan
        return logical_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/policy", response_model=PolicyDecision)
def run_policy(req: PolicyRequest):
    violations = []
    
    routing_data = load_yaml("/app/registry/routing.yaml")
    routing_map = routing_data.get("routing", {})
    
    if req.profile.row_count > 1000000:
        violations.append("Dataset exceeds maximum size limit")
        
    if "Revenue" not in req.profile.columns and "revenue" not in req.profile.columns:
        violations.append("Dataset missing required column: revenue")
        
    for cap in req.capabilities.capabilities:
        if cap not in routing_map:
            violations.append(f"Unknown capability: {cap}")
        else:
            conf = routing_map[cap]
            if "worker" not in conf and "model" not in conf:
                violations.append(f"Worker missing for capability: {cap}")
            if "manifest" not in conf and "worker" in conf:
                pass
                
    if len(req.capabilities.capabilities) > 10:
        violations.append("Parallelism limits exceeded")
        
    policy_passed = len(violations) == 0
    decision_reason = "Policy check passed with no violations." if policy_passed else f"Failed policies: {', '.join(violations)}"
    
    decision = PolicyDecision(
        capabilities=req.capabilities,
        policy_passed=policy_passed,
        violations=violations,
        decision_reason=decision_reason
    )
    _ARTIFACT_STATE['policy_decision'] = decision
    
    if not policy_passed:
        raise HTTPException(status_code=400, detail=decision.model_dump())
        
    return decision

@router.post("/execution-planner", response_model=ExecutionGraph)
async def run_execution_planner(request: Request):
    body = await request.json()
    try:
        req = ExecutionPlannerRequest(**body)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
        
    nodes = []
    edges = []
    
    routing_data = load_yaml("/app/registry/routing.yaml")
    routing_map = routing_data.get("routing", {})
    
    for i, cap in enumerate(req.capabilities.capabilities):
        node_id = f"node_{i}"
        
        tool_config = routing_map.get(cap)
        if not tool_config:
            raise HTTPException(status_code=500, detail=f"Capability {cap} not found in routing")
            
        tool = tool_config.get("worker") or tool_config.get("model")
        worker = tool_config.get("worker", "default_worker")
        
        if not tool or tool == "unknown_tool":
            raise HTTPException(status_code=500, detail=f"Failed to map tool for capability {cap}")
            
        deps = [f"node_{i-1}"] if i > 0 else []
        
        nodes.append(ExecutionNode(
            id=node_id,
            version="1.0",
            capability=cap,
            tool=tool,
            worker=worker,
            manifest_version="1.0",
            dependencies=deps,
            parallel_group=f"group_{i}",
            estimated_cost=0.01,
            estimated_duration=5.0,
            retryable=True,
            timeout_seconds=300,
            priority=1,
            status="PENDING"
        ))
        
        if i > 0:
            edges.append({"from": f"node_{i-1}", "to": node_id})
            
    graph = ExecutionGraph(
        graph_id=str(uuid.uuid4()),
        created_at=datetime.utcnow().isoformat(),
        planner_version="1.0",
        execution_mode="sequential",
        nodes=nodes,
        edges=edges
    )
    _ARTIFACT_STATE['execution_graph'] = graph
    return graph

@router.post("/save-result")
def save_result():
    if 'dataset_profile' not in _ARTIFACT_STATE:
        raise HTTPException(status_code=500, detail="Missing dataset_profile in state")
        
    artifact = PlanningArtifact(
        dataset_profile=_ARTIFACT_STATE['dataset_profile'],
        semantic_model=_ARTIFACT_STATE['semantic_model'],
        logical_plan=_ARTIFACT_STATE['logical_plan'],
        policy_decision=_ARTIFACT_STATE['policy_decision'],
        execution_graph=_ARTIFACT_STATE['execution_graph'],
        metadata={},
        request_id=str(uuid.uuid4()),
        session_id="session_sprint1",
        planner_model="gemini-1.5-pro",
        runtime_version="1.0",
        planning_duration_ms=25000,
        artifact_version="1.0",
        timestamp=datetime.utcnow().isoformat(),
        overall_confidence=_ARTIFACT_STATE['logical_plan'].confidence
    )
    
    with open("/app/shared_libs/planning_result.json", "w") as f:
        f.write(artifact.model_dump_json(indent=2))
        
    return {"status": "success"}
