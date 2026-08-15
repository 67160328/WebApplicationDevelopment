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
        
        def get_ahk_delay_code(val_str: str) -> List[str]:
            if not val_str or val_str == "0.0" or val_str == "0":
                return []
            if "-" in val_str:
                try:
                    parts = val_str.split("-")
                    min_ms = int(float(parts[0].strip()) * 1000)
                    max_ms = int(float(parts[1].strip()) * 1000)
                    return [
                        f"Random, randSleep, {min_ms}, {max_ms}",
                        "Sleep, %randSleep%"
                    ]
                except Exception:
                    pass
            try:
                ms = int(float(val_str) * 1000)
                if ms > 0:
                    return [f"Sleep, {ms}"]
            except Exception:
                pass
            return []

        for step in steps:
            if step.action_type == ActionType.MOUSE_CLICK:
                click_count = step.click_count or 1
                click_interval = step.click_interval or "0.0"
                delay_after = step.delay_after or "0.0"
                
                if click_count > 1 or click_interval != "0.0" or delay_after != "0.0":
                    lines.append(f"Loop, {click_count}")
                    lines.append("{")
                    lines.append(f"    Click, {step.x or 0}, {step.y or 0}")
                    interval_lines = get_ahk_delay_code(click_interval)
                    if interval_lines and click_count > 1:
                        lines.append(f"    if (A_Index < {click_count})")
                        lines.append("    {")
                        for il in interval_lines:
                            lines.append(f"        {il}")
                        lines.append("    }")
                    lines.append("}")
                    delay_lines = get_ahk_delay_code(delay_after)
                    for dl in delay_lines:
                        lines.append(dl)
                else:
                    lines.append(f"Click, {step.x or 0}, {step.y or 0}")
            elif step.action_type == ActionType.KEY_BINDING:
                key_val = step.key or ""
                if "+" in key_val:
                    parts = key_val.split("+")
                    prefix = ""
                    key_part = ""
                    for p in parts:
                        p_lower = p.strip().lower()
                        if p_lower == "ctrl":
                            prefix += "^"
                        elif p_lower == "alt":
                            prefix += "!"
                        elif p_lower == "shift":
                            prefix += "+"
                        elif p_lower == "win":
                            prefix += "#"
                        else:
                            key_part = p.strip()
                    if len(key_part) > 1:
                        lines.append(f"Send, {prefix}{{{key_part}}}")
                    else:
                        lines.append(f"Send, {prefix}{key_part}")
                else:
                    known_keys = {'enter', 'space', 'tab', 'esc', 'escape', 'backspace', 'delete', 'up', 'down', 'left', 'right', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'ctrl', 'alt', 'shift', 'win', 'capslock'}
                    if key_val.lower() in known_keys:
                        lines.append(f"Send, {{{key_val}}}")
                    elif len(key_val) == 1:
                        lines.append(f"Send, {key_val}")
                    else:
                        lines.append(f"SendRaw, {key_val}")
            elif step.action_type == ActionType.DELAY:
                lines.append(f"Sleep, {step.duration_ms or 0}")

        lines.append("Return")
        return "\n".join(lines)
