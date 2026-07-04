import os
import yaml
from pathlib import Path

class ConfigService:
    _cache = {}
    
    @classmethod
    def load(cls, file_name: str, force_reload: bool = False):
        """
        Loads a YAML configuration file from the registry.
        Uses caching to avoid repeated disk reads.
        """
        if file_name in cls._cache and not force_reload:
            return cls._cache[file_name]
            
        from shared_libs.core.config import ConfigService
        base_path = Path(ConfigService.get_registry_path())
        file_path = base_path / file_name
        
        if not file_path.exists():
            # Try alternative path for local dev
            file_path = Path(__file__).parent.parent.parent / "workflows" / "16-registry" / file_name
            
        if not file_path.exists():
            raise FileNotFoundError(f"Configuration file {file_name} not found.")
            
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            cls._cache[file_name] = data
            return data

    @classmethod
    def get_routing(cls):
        return cls.load("routing.yaml").get("routing", {})

    @classmethod
    def get_capabilities(cls):
        return cls.load("capabilities.yaml").get("capabilities", {})
