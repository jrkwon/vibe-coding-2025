import cv2
import os

class FaceDetector:
    def __init__(self, cascade_path=None):
        """
        Initializes the FaceDetector with a Haar Cascade classifier.
        If cascade_path is None, it uses the default OpenCV frontal face cascade.
        """
        if cascade_path is None:
            # Try to locate the default cascade from cv2.data
            cascade_path = os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml')
        
        if not os.path.exists(cascade_path):
             raise FileNotFoundError(f"Haar cascade file not found at: {cascade_path}")

        self.classifier = cv2.CascadeClassifier(cascade_path)

    def detect_face(self, image):
        """
        Detects the largest face in the given image.
        Returns:
            (x, y, w, h) of the largest face, or None if no face is detected.
        """
        if image is None:
            raise ValueError("Image provided to detect_face is None")

        # Convert to grayscale for detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = self.classifier.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        if len(faces) == 0:
            return None

        # Return the largest face (based on area w*h)
        largest_face = max(faces, key=lambda box: box[2] * box[3])
        return largest_face
