import yaml
import os
import logging
from typing import Dict, Any

from shared_libs.core.contracts.execution import Manifest

logger = logging.getLogger("RegistryResolver")

class RegistryResolver:
    def __init__(self, registry_path: str = "/app/registry/routing.yaml"):
        self.registry_path = registry_path
        self.routing = self._load_registry()

    def _load_registry(self) -> Dict[str, Any]:
        if not os.path.exists(self.registry_path):
            raise FileNotFoundError(f"Registry file not found: {self.registry_path}")
        with open(self.registry_path, "r") as f:
            data = yaml.safe_load(f)
        return data.get("routing", {})

    def resolve(self, capability: str) -> Manifest:
        logger.info(f"Resolving capability: {capability}")
        manifest_data = self.routing.get(capability)
        if not manifest_data:
            raise ValueError(f"Capability '{capability}' not found in registry")
        
        try:
            return Manifest(**manifest_data)
        except Exception as e:
            raise ValueError(f"Invalid manifest format for capability '{capability}': {e}")
