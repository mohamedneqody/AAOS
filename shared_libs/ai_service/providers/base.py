from pydantic import BaseModel
from typing import Type, TypeVar

T = TypeVar("T", bound=BaseModel)

class BaseLLMProvider:
    def generate_structured(self, prompt: str, response_model: Type[T], **kwargs) -> T:
        raise NotImplementedError("Subclasses must implement generate_structured")
