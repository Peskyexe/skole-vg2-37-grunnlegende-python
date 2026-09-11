from pathlib import Path
import cv2

def blur_faces(image_path: str) -> str:
    if not image_path.is_file():
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read image (unsupported format?): {image_path}")

    # Converts the image to grayscale for the facial recognition
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Loads OpenCV's built-in Haar Cascade classifier for frontal face detection
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascade_path)

    # Checks for- and saves the positions of faces in the image using the Cascade classifier
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=10, minSize=(65, 65)
    )

    print(f"Faces detected: {len(faces)}")

    # Applies a gaussian blur to all the face's bounding boxes
    for (x, y, w, h) in faces:
        roi = image[y:y + h, x:x + w]
        blurred_roi = cv2.GaussianBlur(roi, (99, 99), 30)
        image[y:y + h, x:x + w] = blurred_roi

    # Saves the new image with the blurred faces
    output_path = image_path.parent / f"{image_path.stem}-blurred{image_path.suffix}"
    cv2.imwrite(output_path, image)
    print(f"Saved blurred image to: {output_path}")

    return output_path

# Gets the file path for the image to scanned and blurred.
image_filename = "test-image.jpg"
script_dir = Path(__file__).resolve().parent
input_path = script_dir / image_filename

blur_faces(input_path)