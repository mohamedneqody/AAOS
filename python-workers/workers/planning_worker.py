import logging
from typing import Dict, Any

logger = logging.getLogger("PlanningWorker")

class PlanningWorker:
    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("PlanningWorker executing")
        return {"status": "SUCCESS", "message": "Executed planning_worker"}
