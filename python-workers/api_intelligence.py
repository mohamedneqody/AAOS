from fastapi import APIRouter, HTTPException
import logging
import traceback

from shared_libs.core.contracts.execution import ExecutionResult
from shared_libs.core.contracts.intelligence import InsightPackage
from intelligence.domain import IntelligenceDomain

logger = logging.getLogger("IntelligenceAPI")
router = APIRouter(prefix="/api/intelligence", tags=["intelligence"])

domain = IntelligenceDomain()

@router.post("/analyze", response_model=InsightPackage)
def analyze_execution(execution: ExecutionResult) -> InsightPackage:
    logger.info(f"Analyzing ExecutionResult: {execution.execution_id}")
    try:
        result = domain.analyze(execution)
        return result
    except Exception as e:
        logger.error(f"Failed to analyze ExecutionResult: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
