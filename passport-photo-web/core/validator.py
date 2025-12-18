import cv2

def validate_image(image_bgr):
    """
    Checks if image meets basic technical compliance.
    Returns (Passed: Bool, Messages: list[str])
    """
    h, w, c = image_bgr.shape
    messages = []
    passed = True
    
    # Check Dimensions
    if h != 600 or w != 600:
        messages.append(f"Dimensions are {w}x{h}, expected 600x600.")
        passed = False
    else:
        messages.append("Dimensions correct (600x600).")
        
    # Future checks: Brightness, Face position, etc.
    
    return passed, messages
