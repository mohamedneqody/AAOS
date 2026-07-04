import logging
from typing import Dict, Any
import uuid

logger = logging.getLogger("PlanningCapability")

class PlanningCapability:
    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("PlanningCapability executing")
        strategy = payload.get("strategy", {})
        
        # Generates deterministic campaign tasks based on strategy
        tasks = []
        raw_goals = strategy.get("Goal Generation", "General Content")
        
        # Create a text generation task
        tasks.append({
            "task_id": str(uuid.uuid4()),
            "type": "content_production",
            "platform": "telegram",
            "topic": str(raw_goals)[:50]
        })
        
        return {
            "status": "SUCCESS", 
            "plan": {
                "campaign_id": str(uuid.uuid4()),
                "tasks": tasks,
                "budget_allocated": strategy.get("budget", 0)
            }
        }
