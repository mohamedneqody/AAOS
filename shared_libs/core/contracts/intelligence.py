from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field

# Base Models
class IntelligenceBase(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: str = "1.0"

# Evidence Models
class EvidenceBundle(IntelligenceBase):
    bundle_id: str
    aggregated_at: str
    evidence_count: int
    valid_hashes: int
    evidence: List[Dict[str, Any]]

# Confidence Models
class ConfidenceMetric(BaseModel):
    model_config = ConfigDict(extra="forbid")
    score: float
    explanation: str

class ConfidenceReport(IntelligenceBase):
    report_id: str
    calculated_at: str
    overall_confidence: ConfidenceMetric
    plugin_confidence: ConfidenceMetric
    evidence_confidence: ConfidenceMetric
    graph_confidence: ConfidenceMetric
    critic_confidence: ConfidenceMetric
    verification_confidence: ConfidenceMetric
    details: Dict[str, Any]

# Knowledge Graph Models
class GraphNode(IntelligenceBase):
    node_id: str
    type: str # Entity, Metric, Business Concept, Insight
    label: str
    properties: Dict[str, Any]

class GraphEdge(IntelligenceBase):
    edge_id: str
    source_id: str
    target_id: str
    relation: str
    weight: float = 1.0
    properties: Dict[str, Any]

class KnowledgeGraphSchema(IntelligenceBase):
    graph_id: str
    nodes: List[GraphNode]
    edges: List[GraphEdge]

# Insight Models
class InsightEvidenceLink(IntelligenceBase):
    evidence_id: str
    relevance: float
    description: str

class BusinessFinding(IntelligenceBase):
    finding_id: str
    title: str
    description: str
    severity: str
    evidence_links: List[InsightEvidenceLink]

class Recommendation(IntelligenceBase):
    recommendation_id: str
    action: str
    expected_impact: str
    evidence_links: List[InsightEvidenceLink]

class Risk(IntelligenceBase):
    risk_id: str
    description: str
    probability: str
    impact: str
    evidence_links: List[InsightEvidenceLink]

class Opportunity(IntelligenceBase):
    opportunity_id: str
    description: str
    potential_value: str
    evidence_links: List[InsightEvidenceLink]

class Insight(IntelligenceBase):
    insight_id: str
    category: str
    summary: str
    findings: List[BusinessFinding] = Field(default_factory=list)
    recommendations: List[Recommendation] = Field(default_factory=list)
    risks: List[Risk] = Field(default_factory=list)
    opportunities: List[Opportunity] = Field(default_factory=list)

class CandidateInsights(IntelligenceBase):
    package_id: str
    generated_at: str
    insights: List[Insight]

# Critic Models
class InsightCriticism(IntelligenceBase):
    insight_id: str
    status: str # approved, rejected, clarification_requested
    reason: str
    contradictions: List[str] = Field(default_factory=list)
    hallucinations: List[str] = Field(default_factory=list)

class CriticReport(IntelligenceBase):
    report_id: str
    evaluated_at: str
    criticisms: List[InsightCriticism]
    total_approved: int
    total_rejected: int

# Final Package
class InsightPackage(IntelligenceBase):
    package_id: str
    planning_id: str
    execution_id: str
    finalized_at: str
    evidence_bundle: EvidenceBundle
    confidence_report: ConfidenceReport
    knowledge_graph: KnowledgeGraphSchema
    critic_report: CriticReport
    verified_insights: List[Insight]
