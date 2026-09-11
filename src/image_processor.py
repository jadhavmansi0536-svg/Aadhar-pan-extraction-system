import cv2


def preprocess_image(image):
    """Enhance an image before OCR processing."""
    if image is None:
        raise ValueError("Invalid image")

    if len(image.shape) == 2:
        gray_image = image
    elif len(image.shape) == 3:
        channels = image.shape[2]
        if channels == 1:
            gray_image = image[:, :, 0]
        elif channels == 3:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        elif channels == 4:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        else:
            raise ValueError(f"Unsupported number of channels: {channels}")
    else:
        raise ValueError("Unsupported image format")

    resized_image = cv2.resize(
        gray_image, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC
    )
    denoised_image = cv2.GaussianBlur(resized_image, (3, 3), 0)
    processed_image = cv2.threshold(
        denoised_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]
    return processed_image
