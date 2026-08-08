from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from app.engine.vision.template_matcher import TemplateMatcherEngine
from app.engine.vision.ocr_engine import OCREngine
from app.engine.vision.object_counter import ObjectCounterEngine

router = APIRouter(prefix="/vision", tags=["Computer Vision & OCR"])

@router.post("/template-match")
async def match_template(
    target_image: UploadFile = File(...),
    template_image: UploadFile = File(...),
    threshold: float = Form(0.8)
):
    """Detect template image coordinates within full screen image."""
    target_bytes = await target_image.read()
    template_bytes = await template_image.read()

    found, coords, confidence = TemplateMatcherEngine.find_template_coordinates(
        target_bytes, template_bytes, threshold
    )
    return {
        "found": found,
        "coordinates": {"x": coords[0], "y": coords[1]} if coords else None,
        "confidence": confidence
    }

@router.post("/ocr")
async def perform_ocr(image: UploadFile = File(...)):
    """Perform OCR text extraction on image."""
    image_bytes = await image.read()
    return OCREngine.extract_text_mock(image_bytes)

@router.post("/count-objects")
async def count_objects(image: UploadFile = File(...), min_area: int = Form(100)):
    """Count matching objects/shapes on image screen."""
    image_bytes = await image.read()
    return ObjectCounterEngine.count_objects(image_bytes, min_area=min_area)
