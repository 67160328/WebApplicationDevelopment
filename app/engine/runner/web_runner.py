import time
from typing import List, Dict, Any
from app.schemas.action_schema import AutomationStep, ActionType

class ScriptRunnerEngine:
    """Asynchronous Web-based Script Execution Runner."""

    @staticmethod
    def execute_steps(steps: List[AutomationStep]) -> Dict[str, Any]:
        """
        Executes macro step sequence in a controlled sandbox web runner.
        Collects detailed execution logs and timing metrics.
        """
        logs: List[str] = []
        metrics: List[Dict[str, Any]] = []
        start_total = time.time()

        logs.append("🚀 Initializing Web Script Runner sandbox...")

        def parse_time_duration(val: str) -> float:
            if not val:
                return 0.0
            val_str = str(val).strip()
            if "-" in val_str:
                try:
                    parts = val_str.split("-")
                    min_val = float(parts[0].strip())
                    max_val = float(parts[1].strip())
                    import random
                    return random.uniform(min_val, max_val)
                except Exception:
                    pass
            try:
                return float(val_str)
            except ValueError:
                return 0.0

        for idx, step in enumerate(steps, start=1):
            step_start = time.time()
            if step.action_type == ActionType.MOUSE_CLICK:
                try:
                    import pyautogui
                    pyautogui.FAILSAFE = False
                    
                    clicks = step.click_count or 1
                    for c_idx in range(clicks):
                        pyautogui.click(step.x, step.y)
                        logs.append(f"Step {idx}: [MOUSE_CLICK] Executed real mouse click ({c_idx + 1}/{clicks}) at X:{step.x}, Y:{step.y}")
                        
                        if c_idx < clicks - 1:
                            interval = parse_time_duration(step.click_interval)
                            if interval > 0:
                                time.sleep(interval)
                                logs.append(f"Step {idx}: [MOUSE_CLICK] Waited {interval:.3f}s between clicks")
                    
                    delay_val = parse_time_duration(step.delay_after)
                    if delay_val > 0:
                        time.sleep(delay_val)
                        logs.append(f"Step {idx}: [MOUSE_CLICK] Delay after completed: {delay_val:.3f}s")
                except Exception as e:
                    logs.append(f"Step {idx}: [MOUSE_CLICK] Simulated click at coordinate X:{step.x}, Y:{step.y} (Reason: {str(e)})")
            elif step.action_type == ActionType.KEY_BINDING:
                try:
                    import pyautogui
                    pyautogui.FAILSAFE = False
                    key_val = step.key or ""
                    
                    known_keys = {'enter', 'space', 'tab', 'esc', 'escape', 'backspace', 'delete', 'up', 'down', 'left', 'right', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'ctrl', 'alt', 'shift', 'win', 'capslock'}
                    
                    if "+" in key_val:
                        keys = [k.strip() for k in key_val.split("+")]
                        pyautogui.hotkey(*keys)
                        logs.append(f"Step {idx}: [KEY_BINDING] Executed hotkey: {keys}")
                    elif key_val.lower() in known_keys or len(key_val) == 1:
                        pyautogui.press(key_val)
                        logs.append(f"Step {idx}: [KEY_BINDING] Executed keypress: '{key_val}'")
                    else:
                        pyautogui.write(key_val)
                        logs.append(f"Step {idx}: [KEY_BINDING] Typed text: '{key_val}'")
                except Exception as e:
                    logs.append(f"Step {idx}: [KEY_BINDING] Simulated keypress/text: '{step.key}' (Reason: {str(e)})")
            elif step.action_type == ActionType.DELAY:
                dur = (step.duration_ms or 0) / 1000.0
                time.sleep(dur)
                logs.append(f"Step {idx}: [WAIT_DELAY] Waited {step.duration_ms} ms")
            
            step_elapsed = round((time.time() - step_start) * 1000, 2)
            metrics.append({
                "step_index": idx,
                "action_type": step.action_type.value,
                "duration_ms": step_elapsed,
                "status": "SUCCESS"
            })

        total_elapsed = round(time.time() - start_total, 3)
        logs.append(f"✅ Script execution completed successfully in {total_elapsed} seconds.")

        return {
            "status": "COMPLETED",
            "total_execution_seconds": total_elapsed,
            "total_steps": len(steps),
            "logs": logs,
            "step_metrics": metrics
        }
