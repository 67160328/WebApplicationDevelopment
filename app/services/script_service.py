from typing import List, Tuple
from app.engine.script_engine import ScriptEngine
from app.schemas.action_schema import AutomationStep

class ScriptService:
    """Service layer orchestrating the isolated Generator Engine with application logic."""

    def __init__(self):
        self.engine = ScriptEngine()

    def generate(self, target_language: str, steps: List[AutomationStep]) -> Tuple[str, str]:
        return self.engine.generate_script(target_language, steps)

    def list_supported_languages(self) -> List[str]:
        return self.engine.get_supported_languages()
