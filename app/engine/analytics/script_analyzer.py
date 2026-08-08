from typing import List, Dict, Any

class ScriptAnalyticsAnalyzer:
    """Performance Analyzer and Diagnostics Engine for automation scripts."""

    @staticmethod
    def analyze_execution(step_metrics: List[Dict[str, Any]], total_seconds: float) -> Dict[str, Any]:
        """
        Analyzes execution step metrics to detect bottlenecks and efficiency metrics.
        """
        if not step_metrics:
            return {
                "efficiency_score": 100,
                "bottleneck_step": None,
                "recommendation": "Script is empty. Add steps to analyze performance."
            }

        slowest_step = max(step_metrics, key=lambda s: s.get("duration_ms", 0))
        total_step_ms = sum(s.get("duration_ms", 0) for s in step_metrics)
        avg_step_ms = round(total_step_ms / len(step_metrics), 2)

        # Calculate efficiency score (100 = optimal, lower = high delay bottlenecks)
        delay_count = sum(1 for s in step_metrics if s.get("action_type") == "delay")
        efficiency_score = max(30, 100 - (delay_count * 10))

        recommendations = []
        if delay_count > 3:
            recommendations.append("Consider replacing fixed delays with Image Detection or OCR conditions for faster response.")
        if slowest_step.get("duration_ms", 0) > 2000:
            recommendations.append(f"Step {slowest_step['step_index']} takes significant time ({slowest_step['duration_ms']} ms). Optimize wait timers.")
        if not recommendations:
            recommendations.append("Script execution profile is optimal with minimal overhead!")

        return {
            "efficiency_score": efficiency_score,
            "average_step_ms": avg_step_ms,
            "slowest_step": slowest_step,
            "total_steps": len(step_metrics),
            "recommendations": recommendations
        }
