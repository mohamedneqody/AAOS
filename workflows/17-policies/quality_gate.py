import logging
from typing import Dict, Any

logger = logging.getLogger("QualityGate")

class QualityGateCapability:
    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("QualityGateCapability executing")
        content = payload.get("content", "")
        issues = []
        severity = "INFO"
        
        # 1. Structural Validation
        if len(content) < 100:
            issues.append("Content length insufficient.")
            severity = "ERROR"
            
        # 2. Policy Validation
        forbidden_words = ["spam", "buy now", "clickbait"]
        if any(word in content.lower() for word in forbidden_words):
            issues.append("Contains policy violation.")
            severity = "FATAL"
            
        # 3. Business Validation
        if "call to action" not in content.lower() and "link" not in content.lower():
            issues.append("Missing business objective / CTA.")
            severity = "WARNING" if severity not in ["ERROR", "FATAL"] else severity
            
        # 4. Quality Scoring
        score = 100
        if severity == "WARNING": score = 80
        elif severity == "ERROR": score = 40
        elif severity == "FATAL": score = 0
            
        # 5. Publishing Readiness
        is_ready = severity in ["INFO", "WARNING"]
        
        return {
            "status": "SUCCESS", 
            "quality_report": {
                "issues": issues,
                "severity": severity,
                "score": score,
                "is_ready": is_ready
            }
        }
