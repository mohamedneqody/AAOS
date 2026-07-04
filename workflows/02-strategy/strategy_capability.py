import logging
import json
from typing import Dict, Any
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared_libs'))
from ai_service.gemini import GeminiService

logger = logging.getLogger("StrategyCapability")

class StrategyCapability:
    def detect_trend_change(self, current_data: Dict, previous_data: Dict) -> bool:
        current_volume = current_data.get("search_volume", 0)
        previous_volume = previous_data.get("search_volume", 0)
        if previous_volume == 0: return True
        return abs(current_volume - previous_volume) / previous_volume > 0.15

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("StrategyCapability executing (Gemini 2.5 Pro)")
        current_data = payload.get("current_market_data", {})
        previous_data = payload.get("previous_market_data", {})
        
        if not self.detect_trend_change(current_data, previous_data):
            logger.info("No trend change. Skipping Pro call.")
            return {"status": "SKIPPED", "strategy": payload.get("previous_strategy")}

        prompt = f"""
        Act as a Strategic Planner. Analyze this market data: {json.dumps(current_data)}
        Generate a comprehensive content strategy.
        Provide:
        1. Goal Generation
        2. Budget Decision
        3. Campaign Creation
        Format as JSON.
        """
        
        try:
            # ONLY use Gemini 2.5 Pro
            result = GeminiService.generate_content(prompt, model_name="gemini-2.5-pro", temperature=0.2)
            
            # Simple JSON extraction (in production, use robust parsing)
            text_content = result["content"]
            if "```json" in text_content:
                text_content = text_content.split("```json")[1].split("```")[0]
            
            try:
                strategy_json = json.loads(text_content)
            except:
                strategy_json = {"raw_strategy": text_content, "budget": 100}

            return {
                "status": "SUCCESS", 
                "strategy": strategy_json,
                "usage": result["usage"],
                "model_used": "gemini_2_5_pro"
            }
        except Exception as e:
            logger.error(f"Strategy failed: {e}")
            return {"status": "FAILED", "reason": str(e)}
