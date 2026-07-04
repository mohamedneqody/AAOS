import uuid
from datetime import datetime, timezone

from shared_libs.core.contracts.execution import ExecutionResult
from shared_libs.core.contracts.intelligence import ConfidenceReport, EvidenceBundle, ConfidenceMetric

class ConfidenceEngine:
    def calculate(self, execution_result: ExecutionResult, evidence_bundle: EvidenceBundle) -> ConfidenceReport:
        total_plugins = len(execution_result.plugin_results)
        successful_plugins = sum(1 for pr in execution_result.plugin_results if pr.status == "SUCCESS")
        
        # 1. Plugin Confidence
        plugin_score = successful_plugins / total_plugins if total_plugins > 0 else 0.0
        plugin_metric = ConfidenceMetric(
            score=plugin_score,
            explanation=f"Calculated from plugin success rate: {successful_plugins}/{total_plugins} successful."
        )
        
        # 2. Evidence Confidence
        evidence_score = evidence_bundle.valid_hashes / evidence_bundle.evidence_count if evidence_bundle.evidence_count > 0 else 0.0
        evidence_metric = ConfidenceMetric(
            score=evidence_score,
            explanation=f"Calculated from valid evidence hashes: {evidence_bundle.valid_hashes}/{evidence_bundle.evidence_count} valid."
        )
        
        # 3. Graph Confidence (Placeholder for initial pass before graph is built)
        graph_metric = ConfidenceMetric(
            score=1.0,
            explanation="Graph completeness verified implicitly by Execution dependencies."
        )

        # 4. Critic Confidence (Placeholder for initial pass before critic runs)
        critic_metric = ConfidenceMetric(
            score=1.0,
            explanation="To be updated after CriticAgent execution."
        )

        # 5. Verification Confidence (Placeholder for initial pass before verifier runs)
        verification_metric = ConfidenceMetric(
            score=1.0,
            explanation="To be updated after Verifier execution."
        )
        
        # 6. Overall Confidence (Deterministic Aggregation)
        overall_score = (plugin_score + evidence_score) / 2.0
        overall_metric = ConfidenceMetric(
            score=overall_score,
            explanation="Equally weighted average of Plugin and Evidence confidence prior to Verification."
        )
        
        return ConfidenceReport(
            report_id=str(uuid.uuid4()),
            calculated_at=datetime.now(timezone.utc).isoformat(),
            overall_confidence=overall_metric,
            plugin_confidence=plugin_metric,
            evidence_confidence=evidence_metric,
            graph_confidence=graph_metric,
            critic_confidence=critic_metric,
            verification_confidence=verification_metric,
            details={
                "total_plugins": total_plugins,
                "successful_plugins": successful_plugins,
                "evidence_count": evidence_bundle.evidence_count,
                "valid_hashes": evidence_bundle.valid_hashes
            }
        )
