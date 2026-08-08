from typing import List
from app.engine.base_generator import BaseScriptGenerator
from app.schemas.action_schema import AutomationStep, ActionType

class BashScriptGenerator(BaseScriptGenerator):
    target_language = "bash"
    file_extension = ".sh"

    def generate(self, steps: List[AutomationStep]) -> str:
        lines = [
            "#!/bin/bash",
            "# Auto-generated Bash Automation Script (Requires xdotool)",
            ""
        ]
        
        for step in steps:
            if step.action_type == ActionType.MOUSE_CLICK:
                lines.append(f"xdotool mousemove {step.x or 0} {step.y or 0} click 1")
            elif step.action_type == ActionType.KEY_BINDING:
                key_val = step.key or ""
                lines.append(f"xdotool key {key_val}")
            elif step.action_type == ActionType.DELAY:
                seconds = (step.duration_ms or 0) / 1000.0
                lines.append(f"sleep {seconds}")

        return "\n".join(lines)
