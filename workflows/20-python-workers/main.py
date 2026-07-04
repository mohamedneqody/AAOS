import os
import sys
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("PythonWorker")

from workers.analytics_worker import AnalyticsWorker
from workers.data_worker import DataWorker
from workers.document_worker import DocumentWorker

# Add capability paths to sys.path since folder names contain dashes
BASE_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(BASE_DIR, '../../workflows/02-strategy'))
sys.path.append(os.path.join(BASE_DIR, '../../workflows/03-planning'))
sys.path.append(os.path.join(BASE_DIR, '../../workflows/10-revenue'))
sys.path.append(os.path.join(BASE_DIR, '../../workflows/06-production'))
sys.path.append(os.path.join(BASE_DIR, '../../workflows/17-policies'))
sys.path.append(os.path.join(BASE_DIR, '../../workflows/08-publishing'))
sys.path.append(os.path.join(BASE_DIR, '../../workflows/14-monitoring'))

from strategy_capability import StrategyCapability
from planning_capability import PlanningCapability
from revenue_validation import RevenueValidationCapability
from production_capability import ProductionCapability
from quality_gate import QualityGateCapability
from telegram_publisher import TelegramPublisherCapability
from kpi_engine import KPIEngineCapability

# ---------------------------------------------------------
# Worker Registry (Dynamic Dispatching)
# ---------------------------------------------------------
worker_registry = {
    "analytics": AnalyticsWorker(),
    "data_manipulation": DataWorker(),
    "document": DocumentWorker(),
    "strategy_planning": StrategyCapability(),
    "planning": PlanningCapability(),
    "revenue_validation": RevenueValidationCapability(),
    "production": ProductionCapability(),
    "quality_gate": QualityGateCapability(),
    "telegram_publisher": TelegramPublisherCapability(),
    "kpi_engine": KPIEngineCapability()
}

def execute(job_type, payload):
    """
    Generic execution function utilizing the dynamic worker_registry.
    """
    logger.info(f"Executing job: {job_type}")
    
    worker = worker_registry.get(job_type)
    if worker:
        try:
            return worker.execute(payload)
        except Exception as e:
            logger.error(f"Error executing {job_type}: {e}")
            return {"status": "FAILED", "message": str(e), "severity": "FATAL"}
            
    return {"status": "FAILED", "message": f"Unknown job_type: {job_type}", "severity": "ERROR"}

def main():
    logger.info("Python Worker Pool starting...")
    logger.info(f"Registered capabilities: {list(worker_registry.keys())}")
    
    # TODO: Implement connection to Postgres Event Queue and fetch jobs via SKIP LOCKED
    while True:
        time.sleep(5)

if __name__ == "__main__":
    main()
