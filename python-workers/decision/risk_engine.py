import uuid
from typing import List
from shared_libs.core.contracts.decision import DecisionContext, RiskAssessment, DecisionTraceability

class RiskEngine:
    def evaluate(self, context: DecisionContext) -> List[RiskAssessment]:
        assessments = []
        insight_pkg = context.insight_package
        planning_id = insight_pkg.planning_id if insight_pkg.planning_id else "TBD_PLAN"
        
        for insight in insight_pkg.verified_insights:
            for risk in insight.risks:
                traceability = DecisionTraceability(
                    planning_id=planning_id,
                    execution_id=insight_pkg.execution_id,
                    insight_id=insight.insight_id,
                    evidence_id=risk.evidence_links[0].evidence_id if risk.evidence_links else "NO_EVIDENCE",
                    decision_id=str(uuid.uuid4()),
                    recommendation_id="PENDING"
                )
                
                assessments.append(RiskAssessment(
                    assessment_id=str(uuid.uuid4()),
                    insight_id=insight.insight_id,
                    category="Operational",  # Fallback deterministic
                    description=risk.description,
                    severity=risk.impact,
                    traceability=traceability
                ))
                
        return assessments
