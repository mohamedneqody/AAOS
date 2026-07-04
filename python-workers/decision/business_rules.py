import uuid
from typing import List
from shared_libs.core.contracts.decision import DecisionContext, BusinessDecision, DecisionTraceability

class BusinessRuleEngine:
    def evaluate(self, context: DecisionContext) -> List[BusinessDecision]:
        decisions = []
        insight_pkg = context.insight_package
        planning_id = insight_pkg.planning_id if insight_pkg.planning_id else "TBD_PLAN"
        
        for insight in insight_pkg.verified_insights:
            for finding in insight.findings:
                # Based on the snippet found in step 5668
                traceability = DecisionTraceability(
                    planning_id=planning_id,
                    execution_id=insight_pkg.execution_id,
                    insight_id=insight.insight_id,
                    evidence_id=finding.evidence_links[0].evidence_id if finding.evidence_links else "NO_EVIDENCE",
                    decision_id=str(uuid.uuid4()),
                    recommendation_id="PENDING"
                )
                
                if finding.severity.lower() in ["high", "critical", "severe"]:
                    decisions.append(BusinessDecision(
                        decision_id=traceability.decision_id,
                        insight_id=insight.insight_id,
                        decision_type="Intervention Required",
                        reasoning=f"High severity finding detected: {finding.title}",
                        status="APPROVED",
                        traceability=traceability
                    ))
                elif "decline" in finding.title.lower() or "drop" in finding.title.lower():
                    decisions.append(BusinessDecision(
                        decision_id=traceability.decision_id,
                        insight_id=insight.insight_id,
                        decision_type="Performance Review",
                        reasoning=f"Negative trend detected: {finding.title}",
                        status="APPROVED",
                        traceability=traceability
                    ))
                else:
                    decisions.append(BusinessDecision(
                        decision_id=traceability.decision_id,
                        insight_id=insight.insight_id,
                        decision_type="Monitor",
                        reasoning=f"Standard finding: {finding.title}",
                        status="APPROVED",
                        traceability=traceability
                    ))
        return decisions
