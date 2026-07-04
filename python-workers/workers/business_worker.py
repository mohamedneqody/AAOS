import logging
import uuid
import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, Any, List

from shared_libs.core.contracts.execution import PluginResult, Evidence

logger = logging.getLogger("BusinessWorker")

class BusinessWorker:
    def __init__(self):
        # Basic rule engine
        self.rules = {
            "pareto": self._compute_pareto,
            "threshold": self._compute_threshold
        }

    def _compute_pareto(self, data: List[Dict[str, Any]], params: Dict[str, Any]) -> Dict[str, Any]:
        if not data: return {"error": "No data"}
        value_key = params.get("value_key", "value")
        sorted_data = sorted(data, key=lambda x: x.get(value_key, 0), reverse=True)
        total = sum(x.get(value_key, 0) for x in data)
        if total == 0: return {"error": "Total is zero"}

        cumulative = 0
        top_80 = []
        for item in sorted_data:
            cumulative += item.get(value_key, 0)
            top_80.append(item)
            if (cumulative / total) >= 0.8:
                break
        return {"top_80_percent_items": len(top_80), "total_items": len(data), "items": top_80}

    def _compute_threshold(self, data: List[Dict[str, Any]], params: Dict[str, Any]) -> Dict[str, Any]:
        threshold = params.get("threshold", 0)
        value_key = params.get("value_key", "value")
        passed = [x for x in data if x.get(value_key, 0) >= threshold]
        return {"passed_count": len(passed), "failed_count": len(data) - len(passed)}

    def execute(self, payload: Dict[str, Any]) -> PluginResult:
        logger.info("BusinessWorker executing")
        start_time = datetime.now(timezone.utc)

        execution_id = payload.get("execution_id", str(uuid.uuid4()))
        graph_id = payload.get("graph_id", "unknown")
        capability = payload.get("capability", "business")
        parameters = payload.get("parameters", {})

        data = parameters.get("data", [])
        rule_name = parameters.get("rule", "pareto")

        if rule_name in self.rules:
            results = self.rules[rule_name](data, parameters)
        else:
            results = {"error": f"Unknown rule {rule_name}"}

        end_time = datetime.now(timezone.utc)
        duration_ms = (end_time - start_time).total_seconds() * 1000

        output_str = json.dumps(results, sort_keys=True)
        computed_hash = hashlib.sha256(output_str.encode('utf-8')).hexdigest()
        confidence = 1.0 if "error" not in results else 0.0

        evidence = Evidence(
            evidence_id=str(uuid.uuid4()),
            execution_id=execution_id,
            graph_id=graph_id,
            worker="business_worker",
            worker_version="1.0",
            tool="python",
            tool_version="3.11",
            capability=capability,
            source="BusinessWorker",
            timestamp=end_time.isoformat(),
            confidence=confidence,
            hash=computed_hash,
            checksum=computed_hash[:16],
            metadata={"rule_applied": rule_name},
            version="1.0"
        )

        return PluginResult(
            version="1.0",
            plugin="business_worker",
            worker="business_worker",
            worker_version="1.0",
            capability=capability,
            status="SUCCESS" if "error" not in results else "FAILED",
            started_at=start_time.isoformat(),
            finished_at=end_time.isoformat(),
            duration_ms=duration_ms,
            confidence=confidence,
            metadata=results,
            evidence=[evidence]
        )