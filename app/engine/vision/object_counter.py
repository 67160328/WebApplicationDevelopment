import cv2
import numpy as np
from typing import Dict, Any, List

class ObjectCounterEngine:
    """OpenCV Contour & Blob Detection Object Counter Engine."""

    @staticmethod
    def count_objects(image_bytes: bytes, min_area: int = 100) -> Dict[str, Any]:
        """
        Detects contours and counts objects matching color/brightness thresholds.
        """
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if img is None:
                return {"count": 0, "objects": []}

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)

            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            detected_objects = []
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area >= min_area:
                    x, y, w, h = cv2.boundingRect(cnt)
                    detected_objects.append({"x": int(x), "y": int(y), "width": int(w), "height": int(h), "area": float(area)})

            return {
                "count": len(detected_objects),
                "objects": detected_objects
            }
        except Exception as e:
            return {"count": 0, "error": str(e)}
