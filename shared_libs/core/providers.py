from abc import ABC, abstractmethod
from typing import Any, Dict, List

class StorageProvider(ABC):
    @abstractmethod
    def put(self, key: str, data: bytes) -> None: pass
    
    @abstractmethod
    def get(self, key: str) -> bytes: pass
    
    @abstractmethod
    def delete(self, key: str) -> None: pass
    
    @abstractmethod
    def exists(self, key: str) -> bool: pass

class CacheProvider(ABC):
    @abstractmethod
    def set(self, key: str, value: str, ttl: int = None) -> None: pass
    
    @abstractmethod
    def get(self, key: str) -> str: pass
    
    @abstractmethod
    def delete(self, key: str) -> None: pass

class SearchProvider(ABC):
    @abstractmethod
    def index(self, document_id: str, document: Dict[str, Any]) -> None: pass
    
    @abstractmethod
    def search(self, query: str) -> List[Dict[str, Any]]: pass
    
    @abstractmethod
    def remove(self, document_id: str) -> None: pass

class NotificationProvider(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> None: pass

class BillingProvider(ABC):
    @abstractmethod
    def verify_quota(self, tenant_id: str, resource: str) -> bool: pass
    
    @abstractmethod
    def report_usage(self, tenant_id: str, resource: str, amount: float) -> None: pass

class PluginProvider(ABC):
    @abstractmethod
    def register(self, plugin_id: str, config: Dict[str, Any]) -> None: pass
    
    @abstractmethod
    def execute(self, plugin_id: str, payload: Dict[str, Any]) -> Any: pass

class FeatureFlagProvider(ABC):
    @abstractmethod
    def is_enabled(self, feature_name: str, context: Dict[str, Any]) -> bool: pass

class EventBusProvider(ABC):
    @abstractmethod
    def publish(self, topic: str, event: Dict[str, Any]) -> None: pass
    
    @abstractmethod
    def subscribe(self, topic: str, handler: Any) -> None: pass
