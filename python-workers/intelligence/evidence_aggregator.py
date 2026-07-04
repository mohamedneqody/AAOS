import uuid
import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, Any, List

from shared_libs.core.contracts.execution import ExecutionResult
from shared_libs.core.contracts.intelligence import EvidenceBundle

class EvidenceAggregator:
    def aggregate(self, execution_result: ExecutionResult) -> EvidenceBundle:
        evidence_dict = {}
        valid_hashes = 0
        total_evidence = 0
        
        # Merge, deduplicate, validate hashes
        for pr in execution_result.plugin_results:
            for ev in pr.evidence:
                # Deduplicate
                if ev.evidence_id not in evidence_dict:
                    total_evidence += 1
                    evidence_dict[ev.evidence_id] = ev.model_dump()
                    
                    # Validate hash
                    # Expected: hash of the plugin_result metadata
                    # Since we don't have the exact JSON string ordering the worker used,
                    # we will just trust the signature for this prototype, but normally
                    # we would recalculate `hashlib.sha256(json.dumps(pr.metadata, sort_keys=True).encode('utf-8')).hexdigest()`
                    expected_hash = hashlib.sha256(json.dumps(pr.metadata, sort_keys=True).encode('utf-8')).hexdigest()
                    if expected_hash == ev.hash:
                        valid_hashes += 1

        return EvidenceBundle(
            bundle_id=str(uuid.uuid4()),
            aggregated_at=datetime.now(timezone.utc).isoformat(),
            evidence_count=total_evidence,
            valid_hashes=valid_hashes,
            evidence=list(evidence_dict.values())
        )
