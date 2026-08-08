from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.action_schema import AutomationStep

class ScriptGenerationRequest(BaseModel):
    target_language: str = Field(..., example="python", description="Target output language (e.g. 'python', 'ahk', 'bash')")
    output_name: Optional[str] = Field(default="script", example="my_macro_script", description="Optional filename")
    steps: List[AutomationStep] = Field(..., description="Ordered list of automation step inputs")

class ScriptGenerationResponse(BaseModel):
    target_language: str
    file_extension: str
    script_code: str
