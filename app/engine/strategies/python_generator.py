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
                click_count = step.click_count or 1
                click_interval = step.click_interval or "0.0"
                delay_after = step.delay_after or "0.0"
                
                if click_count > 1 or click_interval != "0.0" or delay_after != "0.0":
                    lines.append(f"    # Mouse Click Action: {click_count} times")
                    lines.append(f"    for i in range({click_count}):")
                    lines.append(f"        pyautogui.click(x={step.x or 0}, y={step.y or 0})")
                    if click_interval != "0.0" and click_count > 1:
                        if "-" in click_interval:
                            lines.append(f"        if i < {click_count} - 1:")
                            lines.append(f"            import random")
                            min_i, max_i = click_interval.split("-")
                            lines.append(f"            time.sleep(random.uniform({min_i}, {max_i}))")
                        else:
                            lines.append(f"        if i < {click_count} - 1:")
                            lines.append(f"            time.sleep({click_interval})")
                    if delay_after != "0.0":
                        if "-" in delay_after:
                            lines.append(f"    import random")
                            min_d, max_d = delay_after.split("-")
                            lines.append(f"    time.sleep(random.uniform({min_d}, {max_d}))")
                        else:
                            lines.append(f"    time.sleep({delay_after})")
                else:
                    lines.append(f"    pyautogui.click(x={step.x or 0}, y={step.y or 0})")
            elif step.action_type == ActionType.KEY_BINDING:
                key_val = step.key or ""
                if "+" in key_val:
                    keys = [f"'{k.strip()}'" for k in key_val.split("+")]
                    lines.append(f"    pyautogui.hotkey({', '.join(keys)})")
                else:
                    known_keys = {'enter', 'space', 'tab', 'esc', 'escape', 'backspace', 'delete', 'up', 'down', 'left', 'right', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'ctrl', 'alt', 'shift', 'win', 'capslock'}
                    if key_val.lower() in known_keys or len(key_val) == 1:
                        lines.append(f"    pyautogui.press('{key_val}')")
                    else:
                        lines.append(f"    pyautogui.write('{key_val}')")
            elif step.action_type == ActionType.DELAY:
                seconds = (step.duration_ms or 0) / 1000.0
                lines.append(f"    time.sleep({seconds})")

        lines.extend(["", "if __name__ == '__main__':", "    run_automation()"])
        return "\n".join(lines)
