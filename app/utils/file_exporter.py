from fastapi.responses import Response
from typing import Dict

MIME_TYPES: Dict[str, str] = {
    ".py": "text/x-python",
    ".ahk": "text/plain",
    ".sh": "text/x-shellscript",
    ".sql": "application/sql",
    ".json": "application/json"
}

class FileExporterUtil:
    """Utility for preparing downloadable script file HTTP responses."""

    @staticmethod
    def prepare_download_response(content: str, filename: str, extension: str) -> Response:
        clean_ext = extension if extension.startswith(".") else f".{extension}"
        full_filename = f"{filename}{clean_ext}"
        media_type = MIME_TYPES.get(clean_ext, "text/plain")

        headers = {
            "Content-Disposition": f'attachment; filename="{full_filename}"'
        }

        return Response(
            content=content,
            media_type=media_type,
            headers=headers
        )
