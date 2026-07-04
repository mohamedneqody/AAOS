import logging
import sys
import os
from typing import Dict, Any

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared_libs'))
from ai_service.gemini import GeminiService

logger = logging.getLogger("ProductionCapability")

class ProductionCapability:
    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("ProductionCapability executing (Gemini 3.5 Flash)")
        task = payload.get("task", {})
        topic = task.get("topic", "AI Technologies")
        platform = task.get("platform", "telegram")
        
        prompt = f"Write a highly engaging {platform} post about: {topic}. Be concise, use bullet points if necessary, and include a Call to Action."
        
        try:
            # ONLY use Gemini 3.5 Flash for copy generation
            result = GeminiService.generate_content(prompt, model_name="gemini-1.5-flash", temperature=0.8)
            return {
                "status": "SUCCESS", 
                "content": result["content"],
                "usage": result["usage"],
                "model_used": "gemini_3_5_flash"
            }
        except Exception as e:
            logger.error(f"Production failed: {e}")
            return {"status": "FAILED", "reason": str(e)}
