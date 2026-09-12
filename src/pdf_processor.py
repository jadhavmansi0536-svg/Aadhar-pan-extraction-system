import cv2
import numpy as np
import pymupdf


def extract_text_from_pdf(pdf_path):
    """
    Extract digital text directly from a PDF if available (e.g., e-PAN, e-Aadhaar).
    Returns the accumulated text, or None if the PDF has no usable digital text.
    """
    try:
        document = pymupdf.open(pdf_path)
        full_text = []

        for page in document:
            text = page.get_text()
            if text and text.strip():
                full_text.append(text.strip())

        document.close()

        combined = "\n".join(full_text).strip()
        # If there is substantial text, return it
        if len(combined) > 30:
            return combined
        return None
    except Exception:
        return None


def pdf_to_images(pdf_path):
    """
    Convert every PDF page into an OpenCV image.
    """

    document = pymupdf.open(pdf_path)
    images = []

    for page in document:
        pixmap = page.get_pixmap(
            matrix=pymupdf.Matrix(2, 2)
        )

        image_bytes = pixmap.tobytes("png")

        image_array = np.frombuffer(
            image_bytes,
            dtype=np.uint8
        )

        image = cv2.imdecode(
            image_array,
            cv2.IMREAD_COLOR
        )

        images.append(image)

    document.close()

    return images