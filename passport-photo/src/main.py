import argparse
import sys
import os

# Add src to python path to find modules if running from root
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.modules.loader import ImageLoader
from src.modules.detector import FaceDetector
from src.modules.cropper import Cropper
from src.modules.cleaner import BackgroundCleaner
from src.modules.validator import Validator

def main():
    parser = argparse.ArgumentParser(description="Passport Shop - Generate compliant passport photos")
    parser.add_argument("--input", "-i", required=True, help="Path to input image")
    parser.add_argument("--output", "-o", default="output.jpg", help="Path to save output image")
    
    args = parser.parse_args()

    # 1. Load Image
    print(f"Loading image from {args.input}...")
    try:
        image = ImageLoader.load_image(args.input)
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    # 2. Detect Face
    print("Detecting face...")
    detector = FaceDetector()
    face_box = detector.detect_face(image)

    if face_box is None:
        print("Error: No face detected in the image.")
        return
    
    print(f"Face detected at: {face_box}")

    # 3. Crop and Center
    print("Cropping and centering...")
    cropper = Cropper(target_size=(600, 600))
    cropped_image = cropper.crop_to_face(image, face_box)

    # 4. Clean Background
    print("Cleaning background...")
    cleaner = BackgroundCleaner()
    final_image = cleaner.remove_background(cropped_image)

    # 5. Validate
    print("Validating compliance...")
    validator = Validator()
    validation_results = validator.validate(final_image)
    
    for warning in validation_results.get("warnings", []):
        print(f"Warning: {warning}")
        
    if not validation_results["valid"]:
        print("Validation Failed:")
        for error in validation_results.get("errors", []):
            print(f"  - {error}")
        print("Image saved anyway for inspection.")
    else:
        print("Validation Passed.")

    # 6. Save
    print(f"Saving result to {args.output}...")
    ImageLoader.save_image(final_image, args.output)
    print("Done!")

if __name__ == "__main__":
    main()
