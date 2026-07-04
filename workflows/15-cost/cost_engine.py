import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared_libs'))

from core_infrastructure.db import get_connection, release_connection
from observability.logger import get_logger

logger = get_logger("CostEngine")

class CostEngine:
    PRICING = {
        "gemini_2_5_pro": {"prompt_1k": 0.00125, "completion_1k": 0.00375},
        "gemini_3_5_flash": {"prompt_1k": 0.000125, "completion_1k": 0.000375},
        "python_worker": {"per_second": 0.00001}
    }

    @classmethod
    def record_cost(cls, task_id: str, resource_type: str, usage_metrics: dict):
        """
        Calculates and records the cost of a specific task execution.
        """
        api_cost = 0.0
        compute_cost = 0.0
        
        pricing = cls.PRICING.get(resource_type)
        if not pricing:
            logger.warning(f"No pricing found for resource {resource_type}")
            return
            
        if "gemini" in resource_type:
            prompts = usage_metrics.get("prompt_tokens", 0) / 1000.0
            comps = usage_metrics.get("completion_tokens", 0) / 1000.0
            api_cost = (prompts * pricing["prompt_1k"]) + (comps * pricing["completion_1k"])
            
        if resource_type == "python_worker":
            duration_ms = usage_metrics.get("execution_time_ms", 0)
            compute_cost = (duration_ms / 1000.0) * pricing["per_second"]

        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO costs (task_id, resource_type, api_cost, compute_cost)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (task_id, resource_type, api_cost, compute_cost)
                )
                conn.commit()
                logger.info(f"Recorded cost for task {task_id}: API=${api_cost}, Compute=${compute_cost}", 
                            extra={"task_id": task_id})
        except Exception as e:
            conn.rollback()
            logger.error(f"Failed to record cost: {e}")
        finally:
            release_connection(conn)
