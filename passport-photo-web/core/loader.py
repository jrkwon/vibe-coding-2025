import cv2
import numpy as np
from PIL import Image
import io

def load_image_from_bytes(uploaded_file):
    """
    Loads an image from Streamlit UploadedFile (bytes) and converts it to an OpenCV BGR format.
    """
    if uploaded_file is None:
        return None
    
    # Read PIL Image
    image = Image.open(uploaded_file)
    
    # Convert to RGB (in case of RGBA or Greyscale)
    image = image.convert('RGB')
    
    # Convert to NumPy array
    image_np = np.array(image)
    
    # Convert RGB to BGR (OpenCV standard)
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    
    return image_bgr

def convert_opencv_to_pil(image_bgr):
    """
    Converts OpenCV BGR image back to PIL RGB format for display in Streamlit.
    """
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    return Image.fromarray(image_rgb)
