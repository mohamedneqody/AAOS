from typing import List, Dict, Any

from shared_libs.core.contracts.intelligence import CandidateInsights, CriticReport, EvidenceBundle, Insight

class Verifier:
    def verify(self, candidates: CandidateInsights, critic: CriticReport, evidence: EvidenceBundle) -> List[Insight]:
        verified_insights = []
        
        valid_evidence_ids = {ev["evidence_id"] for ev in evidence.evidence}
        critic_approvals = {c.insight_id: c.status == "approved" for c in critic.criticisms}
        
        for insight in candidates.insights:
            # 1. Check Critic Approval
            if not critic_approvals.get(insight.insight_id, False):
                continue
                
            # 2. Check Evidence Link Validities
            evidence_valid = True
            for finding in insight.findings:
                for link in finding.evidence_links:
                    if link.evidence_id not in valid_evidence_ids:
                        evidence_valid = False
                        break
                if not evidence_valid:
                    break
            
            for recommendation in insight.recommendations:
                for link in recommendation.evidence_links:
                    if link.evidence_id not in valid_evidence_ids:
                        evidence_valid = False
                        break
                if not evidence_valid:
                    break
                    
            if not evidence_valid:
                continue
                
            # If all valid, append
            verified_insights.append(insight)
            
        return verified_insights
