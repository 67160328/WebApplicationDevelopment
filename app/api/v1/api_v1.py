from fastapi import APIRouter
from app.api.v1.endpoints.script_router import router as script_router
from app.api.v1.endpoints.health_router import router as health_router
from app.api.v1.endpoints.auth_router import router as auth_router
from app.api.v1.endpoints.user_router import router as user_router

api_v1_router = APIRouter(prefix="/v1")
api_v1_router.include_router(health_router)
api_v1_router.include_router(auth_router)
api_v1_router.include_router(user_router)
api_v1_router.include_router(script_router)
