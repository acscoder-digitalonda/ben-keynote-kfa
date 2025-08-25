from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseProvider(ABC):
    @abstractmethod
    def respond(self, messages: List[Dict[str, str]], model: str, **kwargs) -> str:
        ...
