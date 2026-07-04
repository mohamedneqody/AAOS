import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared_libs'))

from config_service.config import ConfigService
from core_infrastructure.queue_dispatcher import QueueDispatcher

class ModelRouter:
    @staticmethod
    def route_task(task_id: str, capability_name: str, payload: dict):
        routing_rules = ConfigService.get_routing()
        
        rule = routing_rules.get(capability_name)
        if not rule:
            # Fallback based on Golden Rule
            rule = {"model": "gemini_3_5_flash"}
            
        target = rule.get("worker", rule.get("model"))
        
        if target == "python":
            queue_name = "q_python_workers"
        elif target == "gemini_2_5_pro":
            queue_name = "q_llm_pro"
        else:
            queue_name = "q_llm_flash"
            
        # Dispatch
        payload["routed_model"] = target
        return QueueDispatcher.publish(queue_name, payload)
