from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.api.v1.api_v1 import api_v1_router
from app.db.base import Base, engine

# Initialize DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Code & Automation Script Generator API",
    description="Scalable API for generating automation scripts (Python, AutoHotkey, Bash) with Auth & User Management",
    version="1.0.0"
)

# Include API V1 routes
app.include_router(api_v1_router, prefix="/api")

# Mount Static Files (UX/UI Frontend)
static_dir = os.path.join(os.path.dirname(__file__), "app", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def root():
    """Serves the Web UI dashboard."""
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "message": "Code & Automation Script Generator API is running",
        "docs_url": "/docs"
    }
