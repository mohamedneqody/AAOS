import logging
import uuid
import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, List, Any

from shared_libs.core.contracts.execution import (
    ExecutionGraph, ExecutionResult, PluginResult, ExecutionState, ExecutionNode, Evidence
)
from registry_resolver import RegistryResolver
from worker_loader import WorkerLoader

logger = logging.getLogger("Dispatcher")

class DispatcherRuntime:
    def __init__(self):
        import os
        path = "registry/routing.yaml" if os.path.exists("registry/routing.yaml") else "/app/registry/routing.yaml"
        self.registry_resolver = RegistryResolver(registry_path=path)

    def _topological_sort(self, nodes: List[ExecutionNode]) -> List[ExecutionNode]:
        in_degree = {node.id: 0 for node in nodes}
        adj_list = {node.id: [] for node in nodes}
        node_map = {node.id: node for node in nodes}

        for node in nodes:
            for dep in node.dependencies:
                if dep in adj_list:
                    adj_list[dep].append(node.id)
                    in_degree[node.id] += 1
                
        queue = [node_id for node_id, degree in in_degree.items() if degree == 0]
        sorted_nodes = []

        while queue:
            current_id = queue.pop(0)
            sorted_nodes.append(node_map[current_id])
            for neighbor in adj_list[current_id]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(sorted_nodes) != len(nodes):
            raise ValueError("Cycle detected in ExecutionGraph dependencies")

        return sorted_nodes

    def dispatch(self, graph: ExecutionGraph) -> ExecutionResult:
        logger.info(f"Dispatching ExecutionGraph {graph.graph_id}")
        start_time = datetime.now(timezone.utc)
        execution_id = str(uuid.uuid4())
        plugin_results: List[PluginResult] = []
        all_evidence: List[Evidence] = []
        
        status = ExecutionState.SUCCESS.value
        
        try:
            sorted_nodes = self._topological_sort(graph.nodes)
        except Exception as e:
            logger.error(f"Topological sort failed: {e}")
            status = ExecutionState.FAILED.value
            return ExecutionResult(
                execution_id=execution_id,
                graph_id=graph.graph_id,
                status=status,
                started_at=start_time.isoformat(),
                finished_at=datetime.now(timezone.utc).isoformat(),
                duration_ms=0,
                plugin_results=[],
                evidence=[],
                execution_metadata={"error": str(e)}
            )

        # Execute nodes
        for node in sorted_nodes:
            node_start = datetime.now(timezone.utc)
            node.status = ExecutionState.RUNNING.value
            try:
                manifest = self.registry_resolver.resolve(node.capability)
                worker = WorkerLoader.load(manifest)
                
                # Execute worker
                # In Sprint 2, logic was changed to hash the native json.dumps() dict payload
                # and pass node.parameters dynamically
                payload_for_worker = {
                    "execution_id": execution_id,
                    "graph_id": graph.graph_id,
                    "capability": node.capability,
                    "parameters": node.parameters
                }
                output = worker.execute(payload_for_worker)
                
                node_end = datetime.now(timezone.utc)
                duration_ms = (node_end - node_start).total_seconds() * 1000
                
                if isinstance(output, PluginResult):
                    plugin_results.append(output)
                    if output.evidence:
                        all_evidence.extend(output.evidence)
                    if getattr(output, 'status', None) == ExecutionState.FAILED.value:
                        node.status = ExecutionState.FAILED.value
                        status = ExecutionState.FAILED.value
                        break
                    else:
                        node.status = ExecutionState.SUCCESS.value
                    continue
                
                # Cryptographic hashing required by architecture
                payload_bytes = json.dumps(output, sort_keys=True).encode('utf-8')
                crypto_hash = hashlib.sha256(payload_bytes).hexdigest()
                
                evidence = Evidence(
                    evidence_id=str(uuid.uuid4()),
                    execution_id=execution_id,
                    graph_id=graph.graph_id,
                    worker=manifest.worker,
                    worker_version=manifest.version,
                    tool=node.tool,
                    tool_version="1.0",
                    capability=node.capability,
                    source="worker",
                    timestamp=node_end.isoformat(),
                    confidence=1.0,
                    hash=crypto_hash,
                    checksum=crypto_hash[:16],
                    metadata=output
                )
                
                all_evidence.append(evidence)
                
                plugin_result = PluginResult(
                    plugin=manifest.worker,
                    worker=manifest.worker,
                    worker_version=manifest.version,
                    capability=node.capability,
                    status=ExecutionState.SUCCESS.value,
                    started_at=node_start.isoformat(),
                    finished_at=node_end.isoformat(),
                    duration_ms=duration_ms,
                    confidence=1.0,
                    metadata=output,
                    evidence=[evidence]
                )
                
                plugin_results.append(plugin_result)
                node.status = ExecutionState.SUCCESS.value
                
            except Exception as e:
                logger.error(f"Node execution failed for {node.id}: {e}")
                node.status = ExecutionState.FAILED.value
                status = ExecutionState.FAILED.value
                break
                
        end_time = datetime.now(timezone.utc)
        total_duration_ms = (end_time - start_time).total_seconds() * 1000
        
        return ExecutionResult(
            execution_id=execution_id,
            graph_id=graph.graph_id,
            status=status,
            started_at=start_time.isoformat(),
            finished_at=end_time.isoformat(),
            duration_ms=total_duration_ms,
            plugin_results=plugin_results,
            evidence=all_evidence,
            execution_metadata={"nodes_executed": len(plugin_results)}
        )