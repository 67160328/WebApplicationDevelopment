from fastapi import APIRouter
from app.schemas.generator_schema import ScriptGenerationRequest
from app.engine.runner.web_runner import ScriptRunnerEngine
from app.engine.analytics.script_analyzer import ScriptAnalyticsAnalyzer

router = APIRouter(prefix="/runner", tags=["Web Executor & Analytics"])

@router.post("/execute")
async def execute_script_online(payload: ScriptGenerationRequest):
    """Execute script step sequence directly on web sandbox."""
    execution_result = ScriptRunnerEngine.execute_steps(payload.steps)
    analytics_result = ScriptAnalyticsAnalyzer.analyze_execution(
        execution_result["step_metrics"], 
        execution_result["total_execution_seconds"]
    )
    return {
        "execution": execution_result,
        "analytics": analytics_result
    }
