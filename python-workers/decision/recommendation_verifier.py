from typing import List
from shared_libs.core.contracts.decision import DecisionContext, RecommendationDraft, ApprovedRecommendation

class RecommendationVerifier:
    def verify(self, drafts: List[RecommendationDraft], context: DecisionContext, previous: List = None) -> List[ApprovedRecommendation]:
        approved = []
        
        overall_conf = context.insight_package.confidence_report.overall_confidence.score
        if overall_conf < 0.5:
            return []
            
        valid_insight_ids = {i.insight_id for i in context.insight_package.verified_insights}
        valid_evidence_ids = {e.get("evidence_id", "") for e in context.insight_package.evidence_bundle.evidence}
        
        for draft in drafts:
            if draft.traceability.insight_id not in valid_insight_ids:
                continue
                
            if draft.traceability.evidence_id not in valid_evidence_ids:
                continue
                
            approved.append(ApprovedRecommendation(
                recommendation_id=draft.traceability.recommendation_id,
                draft_id=draft.draft_id,
                title=draft.title,
                executive_summary=draft.executive_summary,
                business_reason=draft.business_reason,
                expected_impact=draft.expected_impact,
                priority=1.0,
                effort="Medium",
                confidence=1.0,
                traceability=draft.traceability
            ))
            
        return approved
