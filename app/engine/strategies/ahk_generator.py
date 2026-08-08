from typing import List
from app.engine.base_generator import BaseScriptGenerator
from app.schemas.action_schema import AutomationStep, ActionType

class AHKScriptGenerator(BaseScriptGenerator):
    target_language = "ahk"
    file_extension = ".ahk"

    def generate(self, steps: List[AutomationStep]) -> str:
        lines = [
            "; Auto-generated AutoHotkey (v1.1) Script",
            "#NoEnv",
            "SendMode Input",
            "SetWorkingDir %A_ScriptDir%",
            ""
        ]
        
        for step in steps:
            if step.action_type == ActionType.MOUSE_CLICK:
                lines.append(f"Click, {step.x or 0}, {step.y or 0}")
            elif step.action_type == ActionType.KEY_BINDING:
                key_val = step.key or ""
                lines.append(f"Send, {{{key_val}}}")
            elif step.action_type == ActionType.DELAY:
                lines.append(f"Sleep, {step.duration_ms or 0}")

        lines.append("Return")
        return "\n".join(lines)
