import logging
import uuid
import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, Any

from shared_libs.core.contracts.execution import PluginResult, Evidence

logger = logging.getLogger("AnalyticsWorker")

class AnalyticsWorker:
    def execute(self, payload: Dict[str, Any]) -> PluginResult:
        logger.info("AnalyticsWorker executing")
        start_time = datetime.now(timezone.utc)

        execution_id = payload.get("execution_id", str(uuid.uuid4()))
        graph_id = payload.get("graph_id", "unknown")
        capability = payload.get("capability", "analytics")
        parameters = payload.get("parameters", {})

        data = parameters.get("data", [])

        results = {}
        if data:
            results["count"] = len(data)
            results["sum"] = sum(data)
            results["avg"] = results["sum"] / results["count"]
            results["min"] = min(data)
            results["max"] = max(data)
        else:
            results["error"] = "No data provided"

        end_time = datetime.now(timezone.utc)
        duration_ms = (end_time - start_time).total_seconds() * 1000

        output_str = json.dumps(results, sort_keys=True)
        computed_hash = hashlib.sha256(output_str.encode('utf-8')).hexdigest()
        confidence = min(1.0, len(data) / 100.0) if data else 0.0

        evidence = Evidence(
            evidence_id=str(uuid.uuid4()),
            execution_id=execution_id,
            graph_id=graph_id,
            worker="analytics_worker",
            worker_version="1.0",
            tool="python",
            tool_version="3.11",
            capability=capability,
            source="AnalyticsWorker",
            timestamp=end_time.isoformat(),
            confidence=confidence,
            hash=computed_hash,
            checksum=computed_hash[:16],
            metadata={"data_points": len(data)},
            version="1.0"
        )

        return PluginResult(
            version="1.0",
            plugin="analytics_worker",
            worker="analytics_worker",
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