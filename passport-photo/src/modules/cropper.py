import cv2
import numpy as np

class Cropper:
    def __init__(self, target_size=(600, 600), head_ratio=0.6):
        """
        target_size: (width, height) of the final image.
        head_ratio: Appropriate ratio of head height to image height (US passport rule approx 1 inch to 1 3/8 inch).
        """
        self.target_width, self.target_height = target_size
        self.head_ratio = head_ratio

    def crop_to_face(self, image, face_box):
        """
        Crops the image to center the face, adding padding if necessary.
        face_box: (x, y, w, h)
        """
        if image is None or face_box is None:
            raise ValueError("Invalid input to crop_to_face")

        x, y, w, h = face_box
        img_h, img_w = image.shape[:2]

        # Calculate the center of the face
        face_center_x = x + w // 2
        face_center_y = y + h // 2

        # Start logic:
        # We want the head (h) to occupy 'head_ratio' of the final image height.
        # So, target_crop_height = h / head_ratio
        
        crop_h = int(h / self.head_ratio)
        crop_w = int(crop_h * (self.target_width / self.target_height)) # Maintain aspect ratio of target

        # Calculate crop coordinates centered on face_center
        x1 = face_center_x - crop_w // 2
        y1 = face_center_y - crop_h // 2
        x2 = x1 + crop_w
        y2 = y1 + crop_h

        # Handle padding if crop goes out of bounds
        # Create a new canvas of the crop size, filled with white (or average color)
        # Ideally, we pad with the edge pixels or white. For passport, white is safer if background is already white-ish,
        # but if we crop before cleaning, we might want to replicate or use 0.
        # Let's use constant white padding for simplicity as we will clean background later anyway.
        
        # However, to avoid losing image data, let's extract what we can and place it on a canvas.
        
        canvas = np.full((crop_h, crop_w, 3), 255, dtype=np.uint8) # White canvas

        # Calculate intersection between crop rect and image rect
        src_x1 = max(0, x1)
        src_y1 = max(0, y1)
        src_x2 = min(img_w, x2)
        src_y2 = min(img_h, y2)

        dst_x1 = max(0, src_x1 - x1)
        dst_y1 = max(0, src_y1 - y1)
        dst_x2 = dst_x1 + (src_x2 - src_x1)
        dst_y2 = dst_y1 + (src_y2 - src_y1)

        if src_x2 > src_x1 and src_y2 > src_y1:
            canvas[dst_y1:dst_y2, dst_x1:dst_x2] = image[src_y1:src_y2, src_x1:src_x2]

        # Resize to final target size
        final_image = cv2.resize(canvas, (self.target_width, self.target_height), interpolation=cv2.INTER_AREA)
        
        return final_image
