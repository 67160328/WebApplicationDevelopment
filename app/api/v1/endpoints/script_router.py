from fastapi import APIRouter, HTTPException, status
from app.schemas.generator_schema import ScriptGenerationRequest, ScriptGenerationResponse
from app.services.script_service import ScriptService
from app.utils.file_exporter import FileExporterUtil
from app.core.exceptions import UnsupportedLanguageException

router = APIRouter(prefix="/scripts", tags=["Script Generator"])
script_service = ScriptService()

@router.post(
    "/generate",
    response_model=ScriptGenerationResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Automation Script String"
)
async def generate_script(payload: ScriptGenerationRequest):
    """Receives steps payload and generates target automation script code."""
    try:
        script_code, extension = script_service.generate(
            target_language=payload.target_language,
            steps=payload.steps
        )
        return ScriptGenerationResponse(
            target_language=payload.target_language,
            file_extension=extension,
            script_code=script_code
        )
    except UnsupportedLanguageException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post(
    "/export",
    summary="Generate and Download Automation Script File"
)
async def export_script(payload: ScriptGenerationRequest):
    """Generates target automation script and triggers direct file download."""
    try:
        script_code, extension = script_service.generate(
            target_language=payload.target_language,
            steps=payload.steps
        )
        filename = payload.output_name or "automation_script"
        return FileExporterUtil.prepare_download_response(
            content=script_code,
            filename=filename,
            extension=extension
        )
    except UnsupportedLanguageException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
