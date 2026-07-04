import uuid
from typing import List
from shared_libs.core.contracts.decision import DecisionContext, PriorityScore, DecisionTraceability

class PriorityEngine:
    def evaluate(self, context: DecisionContext) -> List[PriorityScore]:
        scores = []
        insight_pkg = context.insight_package
        planning_id = insight_pkg.planning_id if insight_pkg.planning_id else "TBD_PLAN"
        
        for insight in insight_pkg.verified_insights:
            traceability = DecisionTraceability(
                planning_id=planning_id,
                execution_id=insight_pkg.execution_id,
                insight_id=insight.insight_id,
                evidence_id="AGGREGATED_EVIDENCE",
                decision_id=str(uuid.uuid4()),
                recommendation_id="PENDING"
            )
            
            # Simple deterministic priority logic
            severity_points = sum([2.0 if f.severity.lower() in ['high', 'critical', 'severe'] else 1.0 for f in insight.findings])
            confidence = 1.0
            business_impact = min(10.0, severity_points * 2.0)
            risk = 0.5
            urgency = 0.8 if business_impact > 5.0 else 0.4
            
            final_score = (business_impact * 0.4) + (urgency * 0.4) + (confidence * 0.2)
            
            scores.append(PriorityScore(
                priority_id=str(uuid.uuid4()),
                insight_id=insight.insight_id,
                business_impact=business_impact,
                risk=risk,
                confidence=confidence,
                evidence_coverage=1.0,
                urgency=urgency,
                final_score=final_score
            ))
            
        return scores
