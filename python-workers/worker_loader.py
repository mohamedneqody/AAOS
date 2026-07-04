import importlib
import logging
from typing import Any

from shared_libs.core.contracts.execution import Manifest

logger = logging.getLogger("WorkerLoader")

class WorkerLoader:
    @staticmethod
    def load(manifest: Manifest) -> Any:
        module_name = f"workers.{manifest.worker}"
        class_name = manifest.worker_class
        
        logger.info(f"Loading worker {class_name} from {module_name}")
        
        try:
            module = importlib.import_module(module_name)
            worker_class = getattr(module, class_name)
            return worker_class()
        except ImportError as e:
            raise ImportError(f"Failed to import module {module_name}: {e}")
        except AttributeError as e:
            raise AttributeError(f"Class {class_name} not found in module {module_name}: {e}")
