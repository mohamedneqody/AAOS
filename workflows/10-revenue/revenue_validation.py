import logging
from typing import Dict, Any

logger = logging.getLogger("RevenueValidation")

class RevenueValidationCapability:
    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("RevenueValidationCapability executing")
        strategy = payload.get("strategy", {})
        
        # Check for monetization path
        has_monetization = strategy.get("monetization_links", []) or strategy.get("affiliate_products", [])
        expected_cpc = strategy.get("expected_cpc", 0.0)
        
        if not has_monetization and expected_cpc < 0.5:
            return {"status": "SUCCESS", "validation_state": "REJECTED", "reason": "No monetization path found."}
            
        if has_monetization and expected_cpc >= 1.0:
            return {"status": "SUCCESS", "validation_state": "APPROVED"}
            
        return {"status": "SUCCESS", "validation_state": "NEEDS_REVIEW", "reason": "Monetization exists but metrics are borderline."}
