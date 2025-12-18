import cv2
import numpy as np
from rembg import remove # We will use rembg for high quality removal

def remove_background(image_bgr):
    """
    Removes background using Rembg (U2-Net) and replaces it with white.
    """
    # Rembg expects RGB or RGBA, so we convert
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    
    # Get the image with alpha channel, background transparent
    try:
        output_rgba = remove(image_rgb)
    except Exception as e:
        print("Error in background removal:", e)
        return image_bgr # Fallback if model fails
        
    # Convert to PIL part manually or using numpy
    # output_rgba is a numpy array (H, W, 4)
    
    # Create a white background
    h, w, c = output_rgba.shape
    white_bg = np.full((h, w, 3), 255, dtype=np.uint8)
    
    alpha = output_rgba[:, :, 3] / 255.0
    alpha = alpha[:, :, np.newaxis]
    
    foreground = output_rgba[:, :, :3]
    
    # Composite
    # result = foreground * alpha + white_bg * (1 - alpha)
    result = (foreground * alpha + white_bg * (1.0 - alpha)).astype(np.uint8)
    
    # Convert back to BGR for consistency in pipeline
    result_bgr = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
    
    return result_bgr
