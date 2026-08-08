from abc import ABC, abstractmethod
from typing import List
from app.schemas.action_schema import AutomationStep

class BaseScriptGenerator(ABC):
    """Abstract Strategy interface for target language script generators."""

    @property
    @abstractmethod
    def target_language(self) -> str:
        """Language identifier (e.g. 'python', 'ahk', 'bash', 'sql')."""
        pass

    @property
    @abstractmethod
    def file_extension(self) -> str:
        """File extension associated with the target language (e.g. '.py', '.ahk', '.sh')."""
        pass

    @abstractmethod
    def generate(self, steps: List[AutomationStep]) -> str:
        """Compiles automation steps into a valid script string."""
        pass
