import cv2
import numpy as np
import os

class ImageLoader:
    @staticmethod
    def load_image(image_path):
        """
        Loads an image from the specified path.
        Returns the image in OpenCV format (BGR).
        Raises FileNotFoundError if the file does not exist.
        Raises ValueError if the image cannot be loaded.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at path: {image_path}")
        
        # Read image using cv2
        image = cv2.imread(image_path)
        
        if image is None:
            raise ValueError(f"Failed to load image from path: {image_path}. Format might be unsupported.")
            
        return image

    @staticmethod
    def save_image(image, output_path):
        """
        Saves the image to the specified path.
        """
        success = cv2.imwrite(output_path, image)
        if not success:
             raise IOError(f"Failed to save image to {output_path}")
        return True
