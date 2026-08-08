import cv2
import numpy as np
from typing import Optional, Tuple, Dict, Any

class TemplateMatcherEngine:
    """Computer Vision Template Matcher Engine using OpenCV."""

    @staticmethod
    def find_template_coordinates(
        image_bytes: bytes, 
        template_bytes: bytes, 
        threshold: float = 0.8
    ) -> Tuple[bool, Optional[Tuple[int, int]], float]:
        """
        Locates template image within target image.
        Returns: (found: bool, center_coordinates: (x, y), confidence: float)
        """
        try:
            target_np = np.frombuffer(image_bytes, np.uint8)
            template_np = np.frombuffer(template_bytes, np.uint8)

            img = cv2.imdecode(target_np, cv2.IMREAD_COLOR)
            template = cv2.imdecode(template_np, cv2.IMREAD_COLOR)

            if img is None or template is None:
                return False, None, 0.0

            res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            if max_val >= threshold:
                h, w, _ = template.shape
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                return True, (center_x, center_y), float(max_val)
            
            return False, None, float(max_val)
        except Exception:
            return False, None, 0.0
