from typing import List
from app.engine.base_generator import BaseScriptGenerator
from app.schemas.action_schema import AutomationStep, ActionType

class PythonScriptGenerator(BaseScriptGenerator):
    target_language = "python"
    file_extension = ".py"

    def generate(self, steps: List[AutomationStep]) -> str:
        lines = [
            "# Auto-generated Python Automation Script",
            "# Requirements: pip install pyautogui",
            "import time",
            "import pyautogui",
            "",
            "def run_automation():"
        ]
        
        if not steps:
            lines.append("    pass  # No automation steps provided")
            
        for step in steps:
            if step.action_type == ActionType.MOUSE_CLICK:
                lines.append(f"    pyautogui.click(x={step.x or 0}, y={step.y or 0})")
            elif step.action_type == ActionType.KEY_BINDING:
                key_val = step.key or ""
                lines.append(f"    pyautogui.press('{key_val}')")
            elif step.action_type == ActionType.DELAY:
                seconds = (step.duration_ms or 0) / 1000.0
                lines.append(f"    time.sleep({seconds})")

        lines.extend(["", "if __name__ == '__main__':", "    run_automation()"])
        return "\n".join(lines)
