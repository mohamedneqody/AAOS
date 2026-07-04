import logging
from typing import Dict, Any

logger = logging.getLogger("DocumentWorker")

class DocumentWorker:
    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("DocumentWorker executing")
        return {"status": "SUCCESS", "message": "Executed document_worker"}
