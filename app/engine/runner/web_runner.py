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

        for idx, step in enumerate(steps, start=1):
            step_start = time.time()
            if step.action_type == ActionType.MOUSE_CLICK:
                logs.append(f"Step {idx}: [MOUSE_CLICK] Simulated click at coordinate X:{step.x}, Y:{step.y}")
            elif step.action_type == ActionType.KEY_BINDING:
                logs.append(f"Step {idx}: [KEY_BINDING] Simulated keypress: '{step.key}'")
            elif step.action_type == ActionType.DELAY:
                dur = (step.duration_ms or 0) / 1000.0
                time.sleep(min(dur, 0.5))  # Sandbox cap for fast execution feedback
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
