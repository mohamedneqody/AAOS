import uuid
from typing import List
from shared_libs.core.contracts.decision import DecisionContext, OpportunityAssessment, DecisionTraceability

class OpportunityEngine:
    def evaluate(self, context: DecisionContext) -> List[OpportunityAssessment]:
        assessments = []
        insight_pkg = context.insight_package
        planning_id = insight_pkg.planning_id if insight_pkg.planning_id else "TBD_PLAN"
        
        for insight in insight_pkg.verified_insights:
            for opp in insight.opportunities:
                traceability = DecisionTraceability(
                    planning_id=planning_id,
                    execution_id=insight_pkg.execution_id,
                    insight_id=insight.insight_id,
                    evidence_id=opp.evidence_links[0].evidence_id if opp.evidence_links else "NO_EVIDENCE",
                    decision_id=str(uuid.uuid4()),
                    recommendation_id="PENDING"
                )
                
                assessments.append(OpportunityAssessment(
                    assessment_id=str(uuid.uuid4()),
                    insight_id=insight.insight_id,
                    description=opp.description,
                    potential_value=opp.potential_value,
                    traceability=traceability
                ))
                
        return assessments
