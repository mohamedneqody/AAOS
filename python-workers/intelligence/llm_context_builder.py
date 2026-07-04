import json
from typing import Dict, Any

from shared_libs.core.contracts.execution import ExecutionResult
from shared_libs.core.contracts.intelligence import ConfidenceReport, EvidenceBundle, KnowledgeGraphSchema

class LLMContextBuilder:
    def build_context(self, 
                      execution: ExecutionResult, 
                      confidence: ConfidenceReport, 
                      evidence: EvidenceBundle, 
                      graph: KnowledgeGraphSchema) -> str:
        """
        Builds a structured prompt context containing ONLY the deterministic 
        execution summaries, hiding the raw raw ExecutionResult from the LLM.
        """
        kpi_summaries = {}
        statistical_summaries = {}
        
        for pr in execution.plugin_results:
            if pr.capability in ["analytics", "revenue", "business"]:
                kpi_summaries[pr.capability] = pr.metadata
            elif pr.capability in ["statistics", "forecast"]:
                statistical_summaries[pr.capability] = pr.metadata
                
        context = {
            "execution_status": execution.status,
            "duration_ms": execution.duration_ms,
            "kpi_summaries": kpi_summaries,
            "statistical_summaries": statistical_summaries,
            "confidence_summary": {
                "overall": confidence.overall_confidence.model_dump(),
                "plugin": confidence.plugin_confidence.model_dump(),
                "evidence": confidence.evidence_confidence.model_dump()
            },
            "evidence_summary": {
                "total_evidence": evidence.evidence_count,
                "valid_hashes": evidence.valid_hashes,
                "available_evidence_ids": [ev["evidence_id"] for ev in evidence.evidence]
            },
            "knowledge_graph_summary": {
                "total_nodes": len(graph.nodes),
                "total_edges": len(graph.edges),
                "metrics_tracked": [n.label for n in graph.nodes if n.type == "Metric"]
            }
        }
        
        return json.dumps(context, indent=2)
