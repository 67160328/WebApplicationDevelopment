from typing import Dict, List, Tuple
from app.engine.base_generator import BaseScriptGenerator
from app.engine.strategies.python_generator import PythonScriptGenerator
from app.engine.strategies.ahk_generator import AHKScriptGenerator
from app.engine.strategies.bash_generator import BashScriptGenerator
from app.schemas.action_schema import AutomationStep
from app.core.exceptions import UnsupportedLanguageException

class ScriptEngine:
    """
    Isolated Generator Engine coordinating Target Language strategies.
    Uses Strategy & Factory patterns to decouple business logic.
    """

    def __init__(self):
        self._strategies: Dict[str, BaseScriptGenerator] = {}
        # Register supported strategies
        self.register_strategy(PythonScriptGenerator())
        self.register_strategy(AHKScriptGenerator())
        self.register_strategy(BashScriptGenerator())

    def register_strategy(self, generator: BaseScriptGenerator) -> None:
        """Register a new language generator strategy."""
        self._strategies[generator.target_language.lower()] = generator

    def get_supported_languages(self) -> List[str]:
        """Returns a list of currently registered strategy languages."""
        return list(self._strategies.keys())

    def generate_script(self, target_language: str, steps: List[AutomationStep]) -> Tuple[str, str]:
        """
        Generates code string for target language and returns tuple: (script_code, file_extension)
        """
        strategy = self._strategies.get(target_language.lower())
        if not strategy:
            raise UnsupportedLanguageException(
                f"Target language '{target_language}' is not supported. "
                f"Available languages: {self.get_supported_languages()}"
            )
        
        script_code = strategy.generate(steps)
        return script_code, strategy.file_extension
