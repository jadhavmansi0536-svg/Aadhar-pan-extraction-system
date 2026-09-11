import re


def identify_document(text):
    """Identify whether the document is Aadhaar or PAN."""
    text_upper = text.upper()
    pan_pattern = r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"
    aadhaar_pattern = r"\b\d{4}\s?\d{4}\s?\d{4}\b"

    if re.search(pan_pattern, text_upper):
        return "PAN"
    if re.search(aadhaar_pattern, text_upper):
        return "Aadhaar"
    if "INCOME TAX DEPARTMENT" in text_upper:
        return "PAN"
    if "UNIQUE IDENTIFICATION AUTHORITY" in text_upper:
        return "Aadhaar"
    if "AADHAAR" in text_upper:
        return "Aadhaar"
    return "Unknown"
