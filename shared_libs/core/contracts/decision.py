from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field
from shared_libs.core.contracts.intelligence import InsightPackage

# Base Models
class DecisionBase(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: str = "1.0"

class DecisionTraceability(DecisionBase):
    planning_id: str
    execution_id: str
    insight_id: str
    evidence_id: str
    decision_id: str
    recommendation_id: str

# Context wrapping the Immutable InsightPackage
class DecisionContext(DecisionBase):
    decision_id: str
    started_at: str
    insight_package: InsightPackage

# Priority Engine
class PriorityScore(DecisionBase):
    priority_id: str
    insight_id: str
    business_impact: float
    risk: float
    confidence: float
    evidence_coverage: float
    urgency: float
    final_score: float

# Risk Engine
class RiskAssessment(DecisionBase):
    assessment_id: str
    insight_id: str
    category: str # Financial, Operational, Data, Compliance, Strategic
    description: str
    severity: str
    traceability: DecisionTraceability

# Opportunity Engine
class OpportunityAssessment(DecisionBase):
    assessment_id: str
    insight_id: str
    description: str
    potential_value: str
    traceability: DecisionTraceability

# Business Rule Engine
class BusinessDecision(DecisionBase):
    decision_id: str
    insight_id: str
    decision_type: str
    reasoning: str
    status: str
    traceability: DecisionTraceability

# Recommendation Engine
class RecommendationDraft(DecisionBase):
    draft_id: str
    decision_id: str
    title: str
    executive_summary: str
    business_reason: str
    expected_impact: str
    traceability: DecisionTraceability

# Verified Recommendation
class ApprovedRecommendation(DecisionBase):
    recommendation_id: str
    draft_id: str
    title: str
    executive_summary: str
    business_reason: str
    expected_impact: str
    priority: float
    effort: str
    confidence: float
    traceability: DecisionTraceability

# Action Planner
class BusinessAction(DecisionBase):
    action_id: str
    recommendation_id: str
    owner: str
    category: str
    estimated_duration: str
    estimated_cost: str
    priority: float
    execution_group: str # Phase 1, Phase 2, etc.
    dependencies: List[str]
    status: str
    traceability: DecisionTraceability

# Decision Graph
class GraphNode(DecisionBase):
    node_id: str
    type: str # Decision, Recommendation, Action, Risk, Opportunity, Owner
    label: str

class GraphEdge(DecisionBase):
    edge_id: str
    source_id: str
    target_id: str
    relation: str # Decision -> Recommendation, etc.

class DecisionGraph(DecisionBase):
    graph_id: str
    nodes: List[GraphNode]
    edges: List[GraphEdge]

# Decision Metadata
class DecisionMetadata(DecisionBase):
    decision_time: str
    rules_triggered: int
    insights_used: int
    evidence_used: int
    recommendations_generated: int
    actions_generated: int
    execution_duration: float
    llm_model: str
    llm_tokens: int
    domain_version: str

# Final Package
class DecisionPackage(DecisionBase):
    package_id: str
    planning_id: str
    version: str = "1.0"
    created_at: str
    created_by: str = "AAOS_Decision_Domain"
    domain_version: str = "1.0"
    
    business_decisions: List[BusinessDecision]
    priority_scores: List[PriorityScore]
    risk_assessments: List[RiskAssessment]
    opportunity_assessments: List[OpportunityAssessment]
    approved_recommendations: List[ApprovedRecommendation]
    business_actions: List[BusinessAction]
    decision_graph: DecisionGraph
    decision_metadata: DecisionMetadata
