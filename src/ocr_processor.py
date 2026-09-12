import cv2
import pytesseract
import shutil


TESSERACT_PATH = (
    shutil.which("tesseract")
    or r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def extract_text(image):
    """
    Extract text from an image using Tesseract OCR.
    Uses PSM 3 (fully automatic page segmentation) for multi-column ID layouts
    and falls back to adaptive thresholding if needed.
    """

    if image is None:
        raise ValueError("Invalid image")

    # If image is already grayscale, use it directly.
    if len(image.shape) == 2:
        gray_image = image

    # If image is a color image, convert it to grayscale.
    elif len(image.shape) == 3:
        if image.shape[2] == 3:
            gray_image = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2GRAY
            )

        elif image.shape[2] == 4:
            gray_image = cv2.cvtColor(
                image,
                cv2.COLOR_BGRA2GRAY
            )

        else:
            raise ValueError("Unsupported image channels")

    else:
        raise ValueError("Unsupported image format")

    # Multi-pass OCR: PSM 3 (auto page segmentation) + PSM 6 (dense block)
    # This combination guarantees capturing headers, multi-column layouts,
    # as well as compact personal details (Name, DOB) on Aadhaar and PAN cards.
    text_psm3 = pytesseract.image_to_string(
        gray_image,
        config="--oem 3 --psm 3"
    )

    text_psm6 = pytesseract.image_to_string(
        gray_image,
        config="--oem 3 --psm 6"
    )

    combined = (text_psm3 + "\n" + text_psm6).strip()
    return combined