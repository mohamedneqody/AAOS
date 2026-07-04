import uuid
from typing import List
from shared_libs.core.contracts.decision import DecisionContext, RecommendationDraft, DecisionTraceability

class RecommendationEngine:
    def evaluate(self, context: DecisionContext) -> List[RecommendationDraft]:
        drafts = []
        insight_pkg = context.insight_package
        planning_id = insight_pkg.planning_id if insight_pkg.planning_id else "TBD_PLAN"
        
        for insight in insight_pkg.verified_insights:
            for rec in insight.recommendations:
                traceability = DecisionTraceability(
                    planning_id=planning_id,
                    execution_id=insight_pkg.execution_id,
                    insight_id=insight.insight_id,
                    evidence_id=rec.evidence_links[0].evidence_id if rec.evidence_links else "NO_EVIDENCE",
                    decision_id=str(uuid.uuid4()),
                    recommendation_id=str(uuid.uuid4())
                )
                
                drafts.append(RecommendationDraft(
                    draft_id=str(uuid.uuid4()),
                    decision_id=traceability.decision_id,
                    title=f"Implement: {rec.action}",
                    executive_summary=f"Insight-driven recommendation for {insight.category}",
                    business_reason=insight.summary,
                    expected_impact=rec.expected_impact,
                    traceability=traceability
                ))
                
        return drafts
