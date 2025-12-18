import cv2
import numpy as np

def crop_centered_face(image_bgr, face_bbox, target_size=(600, 600)):
    """
    Crops the image to center the face and reshapes to 600x600.
    US Passport rules typically require the head to be between 1 and 1 3/8 inches.
    2x2 inches total. So head is ~50-69% of height.
    """
    if face_bbox is None:
        return cv2.resize(image_bgr, target_size)

    x, y, w, h = face_bbox
    img_h, img_w = image_bgr.shape[:2]
    
    # Approximate center of the face
    face_cx = x + w // 2
    face_cy = y + h // 2
    
    # Determine the crop size (square). 
    # To satisfy the head size requirement:
    # If the face height (h) is ~60% of the photo height, then PhotoSize = h / 0.6
    desired_crop_dim = int(h / 0.55) # Making it roughly 55% of the image
    
    # Calculate crop coordinates
    x1 = face_cx - desired_crop_dim // 2
    y1 = face_cy - desired_crop_dim // 2
    x2 = x1 + desired_crop_dim
    y2 = y1 + desired_crop_dim
    
    # Pad if out of bounds
    pad_top = max(0, -y1)
    pad_bottom = max(0, y2 - img_h)
    pad_left = max(0, -x1)
    pad_right = max(0, x2 - img_w)
    
    if (pad_top > 0 or pad_bottom > 0 or pad_left > 0 or pad_right > 0):
        image_bgr = cv2.copyMakeBorder(
            image_bgr, pad_top, pad_bottom, pad_left, pad_right, 
            cv2.BORDER_CONSTANT, value=[255, 255, 255]
        )
        # Re-adjust coordinates after padding
        x1 += pad_left
        y1 += pad_top
        x2 += pad_left
        y2 += pad_top
        
    cropped = image_bgr[y1:y2, x1:x2]
    
    # Resize to final build
    final_img = cv2.resize(cropped, target_size, interpolation=cv2.INTER_AREA)
    
    return final_img
