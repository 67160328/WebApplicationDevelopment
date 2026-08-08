from fastapi import APIRouter
from app.services.script_service import ScriptService

router = APIRouter(prefix="/health", tags=["Health"])
service = ScriptService()

@router.get("/")
async def health_check():
    return {
        "status": "online",
        "supported_languages": service.list_supported_languages()
    }
