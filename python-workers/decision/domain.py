import uuid
from datetime import datetime, timezone
from shared_libs.core.contracts.intelligence import InsightPackage
from shared_libs.core.contracts.decision import (
    DecisionPackage, DecisionContext, DecisionMetadata, 
    DecisionGraph, GraphNode, GraphEdge
)

from decision.business_rules import BusinessRuleEngine
from decision.priority_engine import PriorityEngine
from decision.risk_engine import RiskEngine
from decision.opportunity_engine import OpportunityEngine
from decision.recommendation_engine import RecommendationEngine
from decision.recommendation_verifier import RecommendationVerifier
from decision.action_planner import ActionPlanner

class DecisionDomain:
    def __init__(self):
        self.business_rules = BusinessRuleEngine()
        self.priority_engine = PriorityEngine()
        self.risk_engine = RiskEngine()
        self.opportunity_engine = OpportunityEngine()
        self.recommendation_engine = RecommendationEngine()
        self.recommendation_verifier = RecommendationVerifier()
        self.action_planner = ActionPlanner()

    def process(self, insight_package: InsightPackage) -> DecisionPackage:
        start_time = datetime.now(timezone.utc)
        
        # 1. Context Creation
        decision_id = str(uuid.uuid4())
        context = DecisionContext(
            decision_id=decision_id,
            started_at=start_time.isoformat(),
            insight_package=insight_package
        )
        
        # 2. Pure Python Engines
        business_decisions = self.business_rules.evaluate(context)
        priority_scores = self.priority_engine.evaluate(context)
        risk_assessments = self.risk_engine.evaluate(context)
        opportunity_assessments = self.opportunity_engine.evaluate(context)
        
        # 3. LLM Recommendation Formatting (Reconstructed as deterministic)
        drafts = self.recommendation_engine.evaluate(context)
        
        # 4. Pure Python Recommendation Verifier
        approved_recommendations = self.recommendation_verifier.verify(drafts, context)
        
        # 5. Action Planner
        business_actions = self.action_planner.plan(context, approved_recommendations)
        
        # 6. Graph Construction
        nodes = []
        edges = []
        for d in business_decisions:
            nodes.append(GraphNode(node_id=d.decision_id, type="Decision", label=d.decision_type))
            edges.append(GraphEdge(edge_id=str(uuid.uuid4()), source_id=d.insight_id, target_id=d.decision_id, relation="TRIGGERS"))
            
        for r in approved_recommendations:
            nodes.append(GraphNode(node_id=r.recommendation_id, type="Recommendation", label=r.title))
            edges.append(GraphEdge(edge_id=str(uuid.uuid4()), source_id=r.draft_id, target_id=r.recommendation_id, relation="VERIFIED_INTO"))
            
        for action in business_actions:
            nodes.append(GraphNode(node_id=action.action_id, type="Action", label=action.category))
            edges.append(GraphEdge(edge_id=str(uuid.uuid4()), source_id=action.recommendation_id, target_id=action.action_id, relation="IMPLEMENTS"))
            
            owner_id = f"owner_{action.owner}"
            if not any(n.node_id == owner_id for n in nodes):
                nodes.append(GraphNode(node_id=owner_id, type="Owner", label=action.owner))
            edges.append(GraphEdge(edge_id=str(uuid.uuid4()), source_id=action.action_id, target_id=owner_id, relation="ASSIGNED_TO"))
            
        decision_graph = DecisionGraph(
            graph_id=str(uuid.uuid4()),
            nodes=nodes,
            edges=edges
        )
        
        # 7. Metadata
        end_time = datetime.now(timezone.utc)
        duration = (end_time - start_time).total_seconds()
        
        metadata = DecisionMetadata(
            decision_time=end_time.isoformat(),
            rules_triggered=len(business_decisions),
            insights_used=len(context.insight_package.verified_insights),
            evidence_used=context.insight_package.evidence_bundle.evidence_count,
            recommendations_generated=len(approved_recommendations),
            actions_generated=len(business_actions),
            execution_duration=duration,
            llm_model="gemini-2.5-pro",
            llm_tokens=0,
            domain_version="1.0"
        )
        
        # 8. Package Assembly
        return DecisionPackage(
            package_id=str(uuid.uuid4()),
            planning_id=context.insight_package.planning_id if context.insight_package.planning_id else "TBD_PLAN",
            created_at=end_time.isoformat(),
            business_decisions=business_decisions,
            priority_scores=priority_scores,
            risk_assessments=risk_assessments,
            opportunity_assessments=opportunity_assessments,
            approved_recommendations=approved_recommendations,
            business_actions=business_actions,
            decision_graph=decision_graph,
            decision_metadata=metadata
        )