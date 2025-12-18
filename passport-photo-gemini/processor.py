import cv2
import numpy as np
from PIL import Image
import io
from rembg import remove

class PassportProcessor:
    def __init__(self):
        # Load pre-trained face detector from OpenCV
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

    def load_image_from_bytes(self, uploaded_file):
        """Converts uploaded file buffer to an OpenCV image."""
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    def remove_background(self, img):
        """Removes background and replaces it with white."""
        # Convert OpenCV image (numpy) to PIL Image
        pil_img = Image.fromarray(img)
        
        # Remove background (returns image with transparency)
        no_bg_img = remove(pil_img)
        
        # Create a white background image of the same size
        white_bg = Image.new("RGB", no_bg_img.size, (255, 255, 255))
        
        # Paste the no-bg image on top of the white background using alpha channel as mask
        white_bg.paste(no_bg_img, mask=no_bg_img.split()[3])
        
        # Convert back to NumPy array for OpenCV processing
        return np.array(white_bg)

    def detect_face(self, img):
        """Returns the bounding box of the largest face found."""
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) == 0:
            return None
            
        # Return the largest face (x, y, w, h)
        return max(faces, key=lambda rect: rect[2] * rect[3])

    def crop_and_center(self, img, face_box):
        """Crops the image to a square centered on the face with padding."""
        if face_box is None:
            return img
            
        x, y, w, h = face_box
        
        # Calculate center of face
        center_x, center_y = x + w // 2, y + h // 2
        
        # Estimate crop size: 2x face width usually gives good shoulder/head ratio
        crop_size = int(w * 2.0)
        half_crop = crop_size // 2
        
        height, width, _ = img.shape
        
        # Calculate crop coordinates
        start_x = center_x - half_crop
        start_y = center_y - half_crop
        end_x = center_x + half_crop
        end_y = center_y + half_crop

        # Handle padding if crop goes out of bounds (fill with white)
        pad_left = max(0, -start_x)
        pad_top = max(0, -start_y)
        pad_right = max(0, end_x - width)
        pad_bottom = max(0, end_y - height)
        
        # Create a white canvas large enough for the full crop
        padded_h = height + pad_top + pad_bottom
        padded_w = width + pad_left + pad_right
        padded_img = np.full((padded_h, padded_w, 3), 255, dtype=np.uint8)
        
        # Place original image into padded canvas
        padded_img[pad_top:pad_top+height, pad_left:pad_left+width] = img
        
        # Perform the crop on the padded image
        new_start_x = start_x + pad_left
        new_start_y = start_y + pad_top
        
        return padded_img[new_start_y:new_start_y+crop_size, new_start_x:new_start_x+crop_size]

    def resize_image(self, img, size=(600, 600)):
        """Resizes image to strict 600x600 pixels."""
        return cv2.resize(img, size, interpolation=cv2.INTER_AREA)

    def validate_image(self, img):
        """Simple compliance check."""
        h, w, _ = img.shape
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        avg_brightness = np.mean(gray)
        
        issues = []
        if h != 600 or w != 600:
            issues.append(f"Incorrect Size: {w}x{h} (Required: 600x600)")
        if avg_brightness < 50:
            issues.append("Image is too dark")
        if avg_brightness > 240: # Higher threshold since bg is white
            issues.append("Image might be washed out")
            
        return issues

    def convert_to_bytes(self, img):
        """Converts processed NumPy image back to bytes."""
        pil_img = Image.fromarray(img)
        buf = io.BytesIO()
        pil_img.save(buf, format="JPEG", quality=95)
        return buf.getvalue()