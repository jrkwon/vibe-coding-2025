import cv2
import os

def detect_face_bbox(image_bgr):
    """
    Detects the largest face in the image using Haar Cascade.
    Returns the bounding box (x, y, w, h) or None if no face found.
    """
    
    # Load Haar Cascade
    # We use the standard haarcascade_frontalface_default.xml included in cv2 or local
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)
    
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    
    if len(faces) == 0:
        return None
        
    # Assume the largest face is the target
    best_face = max(faces, key=lambda rect: rect[2] * rect[3])
    return best_face
