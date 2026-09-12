import cv2
import numpy as np
from PIL import Image, ImageOps


def load_image(file_path):
    """
    Safely load an image from disk while respecting EXIF orientation
    (common in photos taken with smartphones).
    """
    try:
        pil_image = Image.open(file_path)
        pil_image = ImageOps.exif_transpose(pil_image)

        if pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")

        open_cv_image = np.array(pil_image)
        # Convert RGB to BGR for OpenCV
        return cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)
    except Exception:
        # Fallback to direct OpenCV reading
        return cv2.imread(file_path)


def to_grayscale(image):
    """
    Convert any image to a single-channel grayscale image.
    """
    if image is None:
        raise ValueError("Invalid image")

    if len(image.shape) == 2:
        return image

    if len(image.shape) == 3:
        channels = image.shape[2]
        if channels == 1:
            return image[:, :, 0]
        elif channels == 3:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        elif channels == 4:
            return cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)

    raise ValueError("Unsupported image format")


def resize_for_ocr(gray_image, target_width=1600):
    """
    Standardize image dimensions for optimal OCR accuracy.
    Avoids over-scaling large phone photos and upscales low-res scans.
    """
    h, w = gray_image.shape[:2]
    if w == 0 or h == 0:
        return gray_image

    if w < 1100:
        scale = target_width / float(w)
        return cv2.resize(
            gray_image,
            None,
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_CUBIC
        )
    elif w > 2400:
        scale = target_width / float(w)
        return cv2.resize(
            gray_image,
            None,
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_AREA
        )

    return gray_image


def preprocess_image(image):
    """
    Enhance an image before OCR processing.
    Converts to grayscale for optimal Tesseract OCR engine performance.
    """
    gray = to_grayscale(image)
    return gray



def get_adaptive_threshold(gray_image):
    """
    Fallback adaptive thresholding for tough images with heavy backgrounds.
    """
    return cv2.adaptiveThreshold(
        gray_image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        25,
        12
    )