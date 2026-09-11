import pymupdf


def pdf_to_images(pdf_path):
    """Convert every PDF page into an OpenCV image."""
    document = pymupdf.open(pdf_path)
    images = []

    for page in document:
        pixmap = page.get_pixmap(matrix=pymupdf.Matrix(2, 2))
        image_bytes = pixmap.tobytes("png")

        import numpy as np
        import cv2

        image_array = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        images.append(image)

    document.close()
    return images
