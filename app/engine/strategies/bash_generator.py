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
        
        def get_bash_delay_code(val_str: str) -> List[str]:
            if not val_str or val_str == "0.0" or val_str == "0":
                return []
            if "-" in val_str:
                try:
                    parts = val_str.split("-")
                    min_val = float(parts[0].strip())
                    max_val = float(parts[1].strip())
                    return [f"sleep $(awk -v min={min_val} -v max={max_val} 'BEGIN{{srand(); print min+rand()*(max-min)}}')"]
                except Exception:
                    pass
            try:
                seconds = float(val_str)
                if seconds > 0:
                    return [f"sleep {seconds}"]
            except Exception:
                pass
            return []

        for step in steps:
            if step.action_type == ActionType.MOUSE_CLICK:
                click_count = step.click_count or 1
                click_interval = step.click_interval or "0.0"
                delay_after = step.delay_after or "0.0"
                
                if click_count > 1 or click_interval != "0.0" or delay_after != "0.0":
                    lines.append(f"for i in $(seq 1 {click_count}); do")
                    lines.append(f"    xdotool mousemove {step.x or 0} {step.y or 0} click 1")
                    interval_lines = get_bash_delay_code(click_interval)
                    if interval_lines and click_count > 1:
                        lines.append(f"    if [ $i -lt {click_count} ]; then")
                        for il in interval_lines:
                            lines.append(f"        {il}")
                        lines.append("    fi")
                    lines.append("done")
                    delay_lines = get_bash_delay_code(delay_after)
                    for dl in delay_lines:
                        lines.append(dl)
                else:
                    lines.append(f"xdotool mousemove {step.x or 0} {step.y or 0} click 1")
            elif step.action_type == ActionType.KEY_BINDING:
                key_val = step.key or ""
                known_keys = {'enter', 'space', 'tab', 'esc', 'escape', 'backspace', 'delete', 'up', 'down', 'left', 'right', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'ctrl', 'alt', 'shift', 'win', 'capslock'}
                if "+" in key_val or key_val.lower() in known_keys or len(key_val) == 1:
                    lines.append(f"xdotool key {key_val}")
                else:
                    lines.append(f"xdotool type \"{key_val}\"")
            elif step.action_type == ActionType.DELAY:
                seconds = (step.duration_ms or 0) / 1000.0
                lines.append(f"sleep {seconds}")

        return "\n".join(lines)
