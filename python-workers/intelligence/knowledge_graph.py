from abc import ABC, abstractmethod
import uuid
from typing import List, Dict, Any

from shared_libs.core.contracts.execution import ExecutionResult
from shared_libs.core.contracts.intelligence import KnowledgeGraphSchema, GraphNode, GraphEdge

class IKnowledgeGraph(ABC):
    @abstractmethod
    def build_from_execution(self, execution_result: ExecutionResult) -> KnowledgeGraphSchema:
        pass

class InMemoryKnowledgeGraph(IKnowledgeGraph):
    def build_from_execution(self, execution_result: ExecutionResult) -> KnowledgeGraphSchema:
        nodes = []
        edges = []
        
        # Add a central execution node
        execution_node_id = f"execution_{execution_result.execution_id}"
        nodes.append(GraphNode(
            node_id=execution_node_id,
            type="Execution",
            label="Execution Run",
            properties={"status": execution_result.status, "duration_ms": execution_result.duration_ms}
        ))
        
        # Add Metrics and Business Concepts for each capability
        for pr in execution_result.plugin_results:
            metric_node_id = f"metric_{pr.capability}_{pr.plugin}"
            nodes.append(GraphNode(
                node_id=metric_node_id,
                type="Metric",
                label=pr.capability.title(),
                properties={"status": pr.status, "confidence": pr.confidence}
            ))
            
            # Link Execution to Metric
            edges.append(GraphEdge(
                edge_id=str(uuid.uuid4()),
                source_id=execution_node_id,
                target_id=metric_node_id,
                relation="PRODUCED_METRIC",
                properties={"worker": pr.worker}
            ))
            
            # Add Evidence Nodes
            for ev in pr.evidence:
                evidence_node_id = f"evidence_{ev.evidence_id}"
                nodes.append(GraphNode(
                    node_id=evidence_node_id,
                    type="Evidence",
                    label=f"Evidence: {ev.source}",
                    properties={"hash": ev.hash, "checksum": ev.checksum}
                ))
                
                # Link Metric to Evidence
                edges.append(GraphEdge(
                    edge_id=str(uuid.uuid4()),
                    source_id=metric_node_id,
                    target_id=evidence_node_id,
                    relation="BACKED_BY",
                    properties={"confidence": ev.confidence}
                ))
                
        return KnowledgeGraphSchema(
            graph_id=str(uuid.uuid4()),
            nodes=nodes,
            edges=edges
        )

# Factory or direct export
def get_knowledge_graph_builder() -> IKnowledgeGraph:
    return InMemoryKnowledgeGraph()
