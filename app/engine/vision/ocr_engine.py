import cv2
import numpy as np
from typing import Dict, Any, List

class OCREngine:
    """Optical Character Recognition & Pattern Extraction Engine."""

    @staticmethod
    def extract_text_mock(image_bytes: bytes) -> Dict[str, Any]:
        """
        Extracts recognized text lines and bounding boxes from image buffer.
        """
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                return {"text": "", "words": []}

            # Preprocessing image (grayscale & thresholding)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
            
            return {
                "text": "SUCCESS: LOGIN COMPLETED",
                "confidence": 0.95,
                "detected_words": ["SUCCESS:", "LOGIN", "COMPLETED"]
            }
        except Exception as e:
            return {"text": "", "error": str(e)}
