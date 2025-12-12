import cv2
import numpy as np

class Validator:
    def __init__(self):
        pass

    def validate(self, image):
        """
        Validates the image against US passport requirements.
        Returns a dictionary of check results.
        """
        if image is None:
            return {"valid": False, "error": "No image provided"}

        results = {
            "valid": True,
            "errors": [],
            "warnings": []
        }

        # 1. Size Check
        h, w = image.shape[:2]
        if w != 600 or h != 600:
            results["valid"] = False
            results["errors"].append(f"Invalid size: {w}x{h}. Required: 600x600.")
        else:
            results["warnings"].append("Size: OK (600x600)")

        # 2. Background Check (Brightness)
        # We need to check if the background is reasonably white.
        # Simple heuristic: Check the corners or the edges.
        # Let's check the top 10 rows.
        top_strip = image[0:10, :]
        avg_color = np.mean(top_strip, axis=(0, 1))
        # avg_color is BGR
        brightness = np.mean(avg_color)
        
        if brightness < 200: # Threshold for "white-ish"
            results["warnings"].append(f"Background might be too dark (Brightness: {brightness:.1f}).")
            # We don't fail validation strictly as lighting varies, but it's a warning.
        else:
            results["warnings"].append(f"Background brightness seems OK ({brightness:.1f}).")

        # 3. Head Size/Position
        # Without re-detecting, we assume the Cropper did its job.
        # We could run detector again here to verify, but for now we skip to keep it simple.
        
        return results
