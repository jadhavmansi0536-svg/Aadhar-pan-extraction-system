import cv2
import pytesseract
import shutil

TESSERACT_PATH = (
    shutil.which("tesseract")
    or r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def extract_text(image):
    """Extract text from an image using Tesseract OCR."""
    if image is None:
        raise ValueError("Invalid image")

    if len(image.shape) == 2:
        gray_image = image
    elif len(image.shape) == 3:
        if image.shape[2] == 3:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        elif image.shape[2] == 4:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        else:
            raise ValueError("Unsupported image channels")
    else:
        raise ValueError("Unsupported image format")

    processed_image = cv2.threshold(
        gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]
    text = pytesseract.image_to_string(processed_image, config="--psm 6")
    return text.strip()
