import logging
import uuid
import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, Any, List

from shared_libs.core.contracts.execution import PluginResult, Evidence

logger = logging.getLogger("ForecastWorker")

class ForecastWorker:
    def __init__(self):
        self.algorithms = {
            "SMA": self._compute_sma
        }

    def _compute_sma(self, data: List[float], window: int) -> List[float]:
        if not data or window <= 0:
            return []
        result = []
        for i in range(len(data) - window + 1):
            window_slice = data[i : i + window]
            result.append(sum(window_slice) / window)
        return result

    def execute(self, payload: Dict[str, Any]) -> PluginResult:
        logger.info("ForecastWorker executing")
        start_time = datetime.now(timezone.utc)

        execution_id = payload.get("execution_id", str(uuid.uuid4()))
        graph_id = payload.get("graph_id", "unknown")
        capability = payload.get("capability", "forecast")
        parameters = payload.get("parameters", {})

        data = parameters.get("data", [])
        algo = parameters.get("algorithm", "SMA")

        results = {}
        if algo in self.algorithms:
            results["forecast"] = self.algorithms[algo](data, parameters.get("window", 3))
            if not results["forecast"]:
                results["error"] = "Insufficient data for window"
        else:
            results["error"] = f"Unsupported algorithm: {algo}"

        end_time = datetime.now(timezone.utc)
        duration_ms = (end_time - start_time).total_seconds() * 1000

        output_str = json.dumps(results, sort_keys=True)
        computed_hash = hashlib.sha256(output_str.encode('utf-8')).hexdigest()
        confidence = 1.0 if len(data) >= parameters.get("window", 3) else 0.0

        evidence = Evidence(
            evidence_id=str(uuid.uuid4()),
            execution_id=execution_id,
            graph_id=graph_id,
            worker="forecast_worker",
            worker_version="1.0",
            tool="python",
            tool_version="3.11",
            capability=capability,
            source="ForecastWorker",
            timestamp=end_time.isoformat(),
            confidence=confidence,
            hash=computed_hash,
            checksum=computed_hash[:16],
            metadata={"algorithm": algo},
            version="1.0"
        )

        return PluginResult(
            version="1.0",
            plugin="forecast_worker",
            worker="forecast_worker",
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