import uuid
from typing import List
from shared_libs.core.contracts.decision import DecisionContext, ApprovedRecommendation, BusinessAction

class ActionPlanner:
    def plan(self, context: DecisionContext, recommendations: List[ApprovedRecommendation]) -> List[BusinessAction]:
        actions = []
        
        for rec in recommendations:
            actions.append(BusinessAction(
                action_id=str(uuid.uuid4()),
                recommendation_id=rec.recommendation_id,
                owner="SYSTEM",
                category="Auto-Generated",
                estimated_duration="1 Sprint",
                estimated_cost="0",
                priority=rec.priority,
                execution_group="Phase 1",
                dependencies=[],
                status="PLANNED",
                traceability=rec.traceability
            ))
            
        return actions
