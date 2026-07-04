import uuid
from datetime import datetime, timezone

from shared_libs.core.contracts.execution import ExecutionResult
from shared_libs.core.contracts.intelligence import InsightPackage

from .evidence_aggregator import EvidenceAggregator
from .confidence_engine import ConfidenceEngine
from .knowledge_graph import get_knowledge_graph_builder
from .llm_context_builder import LLMContextBuilder
from .insight_engine import InsightEngine
from .critic_agent import CriticAgent
from .verifier import Verifier

class IntelligenceDomain:
    def __init__(self):
        self.evidence_aggregator = EvidenceAggregator()
        self.confidence_engine = ConfidenceEngine()
        self.kg_builder = get_knowledge_graph_builder()
        self.context_builder = LLMContextBuilder()
        self.insight_engine = InsightEngine()
        self.critic_agent = CriticAgent()
        self.verifier = Verifier()

    def analyze(self, execution_result: ExecutionResult) -> InsightPackage:
        # 1. Aggregate Evidence
        evidence_bundle = self.evidence_aggregator.aggregate(execution_result)
        
        # 2. Compute Confidence
        confidence_report = self.confidence_engine.calculate(execution_result, evidence_bundle)
        
        # 3. Build Knowledge Graph
        knowledge_graph = self.kg_builder.build_from_execution(execution_result)
        
        # 4. Build Context for LLM
        context_str = self.context_builder.build_context(
            execution=execution_result,
            confidence=confidence_report,
            evidence=evidence_bundle,
            graph=knowledge_graph
        )
        
        # 5. Generate Candidate Insights
        candidate_insights = self.insight_engine.generate(context_str)
        
        # 6. Criticize Insights
        critic_report = self.critic_agent.evaluate(candidate_insights, context_str)
        
        # Update critic confidence based on approval rate
        total_criticized = len(critic_report.criticisms)
        critic_conf = critic_report.total_approved / total_criticized if total_criticized > 0 else 1.0
        confidence_report.critic_confidence.score = critic_conf
        confidence_report.critic_confidence.explanation = f"Critic approved {critic_report.total_approved}/{total_criticized} insights."
        
        # 7. Verify Insights deterministically
        verified_insights = self.verifier.verify(candidate_insights, critic_report, evidence_bundle)
        
        # Update verification confidence based on drop-off rate
        total_candidates = len(candidate_insights.insights)
        verification_conf = len(verified_insights) / total_candidates if total_candidates > 0 else 1.0
        confidence_report.verification_confidence.score = verification_conf
        confidence_report.verification_confidence.explanation = f"Verifier approved {len(verified_insights)}/{total_candidates} insights."
        
        # Update overall
        confidence_report.overall_confidence.score = (
            confidence_report.plugin_confidence.score +
            confidence_report.evidence_confidence.score +
            confidence_report.critic_confidence.score +
            confidence_report.verification_confidence.score
        ) / 4.0
        confidence_report.overall_confidence.explanation = "Equally weighted average of Plugin, Evidence, Critic, and Verification confidence."
        
        # 8. Assemble final package
        return InsightPackage(
            package_id=str(uuid.uuid4()),
            planning_id=execution_result.graph_id,
            execution_id=execution_result.execution_id,
            finalized_at=datetime.now(timezone.utc).isoformat(),
            evidence_bundle=evidence_bundle,
            confidence_report=confidence_report,
            knowledge_graph=knowledge_graph,
            critic_report=critic_report,
            verified_insights=verified_insights
        )
