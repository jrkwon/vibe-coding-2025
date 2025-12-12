import cv2
import numpy as np

class BackgroundCleaner:
    def __init__(self):
        pass

    def remove_background(self, image):
        """
        Removes the background from the image and replaces it with white.
        Uses OpenCV GrabCut algorithm.
        """
        if image is None:
            raise ValueError("Input image is None")

        # Create a mask
        mask = np.zeros(image.shape[:2], np.uint8)

        # Define the rectangle for GrabCut
        # Since we already cropped to the face (and ample shoulders), we can assume the central part is FG.
        # Let's define a rect that excludes a small border.
        h, w = image.shape[:2]
        margin = 2
        rect = (margin, margin, w - 2*margin, h - 2*margin)

        # Allocate arrays for internal GrabCut models
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)

        # Run GrabCut
        # iterCount=5 is a reasonable trade-off for speed/accuracy
        try:
            cv2.grabCut(image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
        except Exception as e:
            print(f"Warning: GrabCut failed: {e}. Returning original image.")
            return image

        # Modify mask: 0 and 2 are background, 1 and 3 are foreground
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

        # Create white background
        white_bg = np.full(image.shape, 255, dtype=np.uint8)
        
        # Combine image and white background using the mask
        # image * mask2[:, :, np.newaxis] keeps the FG
        # white_bg * (1 - mask2[:, :, np.newaxis]) keeps the BG
        
        img_fg = image * mask2[:, :, np.newaxis]
        bg_part = white_bg * (1 - mask2[:, :, np.newaxis])
        
        final_image = cv2.add(img_fg, bg_part)

        return final_image
