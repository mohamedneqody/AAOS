from fastapi import APIRouter, HTTPException
import logging
import traceback

from shared_libs.core.contracts.execution import ExecutionGraph, ExecutionResult
from dispatcher import DispatcherRuntime

logger = logging.getLogger("ExecutionAPI")
router = APIRouter(prefix="/api/execution", tags=["execution"])

dispatcher = DispatcherRuntime()

@router.post("/dispatch", response_model=ExecutionResult)
def dispatch_execution(graph: ExecutionGraph) -> ExecutionResult:
    logger.info(f"Received ExecutionGraph: {graph.graph_id}")
    try:
        result = dispatcher.dispatch(graph)
        return result
    except Exception as e:
        logger.error(f"Failed to dispatch ExecutionGraph: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
