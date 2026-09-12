import re


def identify_document(text):
    """
    Identify whether the document is Aadhaar or PAN, even with noisy OCR text.
    """
    if not text:
        return "Unknown"

    text_upper = text.upper()

    # Exact standard patterns
    pan_pattern = r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"
    aadhaar_pattern = r"\b\d{4}\s\d{4}\s\d{4}\b"
    aadhaar_unspaced = r"\b\d{12}\b"

    pan_score = 0
    aadhaar_score = 0

    # Check PAN pattern
    if re.search(pan_pattern, text_upper):
        pan_score += 10

    # Check Aadhaar pattern
    if re.search(aadhaar_pattern, text_upper):
        aadhaar_score += 10
    elif re.search(aadhaar_unspaced, text_upper):
        aadhaar_score += 6

    # PAN Keywords
    pan_keywords = [
        "INCOME TAX DEPARTMENT",
        "INCOMETAX",
        "INCOME TAX",
        "TAX DEPARTMENT",
        "PERMANENT ACCOUNT NUMBER",
        "ACCOUNT NUMBER CARD",
        "आयकर विभाग",
        "स्थायी लेखा संख्या",
        "UTIITSL",
        "NSDL"
    ]
    for kw in pan_keywords:
        if kw in text_upper:
            pan_score += 4

    if re.search(r"FATHER'?S?\s+NAME", text_upper):
        pan_score += 2

    # Aadhaar Keywords
    aadhaar_keywords = [
        "UNIQUE IDENTIFICATION AUTHORITY",
        "UIDAI",
        "AADHAAR",
        "AADHAR",
        "MERA AADHAAR",
        "MERI PEHCHAN",
        "भारतीय विशिष्ट पहचान",
        "आधार",
        "ENROLMENT NO"
    ]
    for kw in aadhaar_keywords:
        if kw in text_upper:
            aadhaar_score += 4

    if pan_score > aadhaar_score and pan_score >= 4:
        return "PAN"
    if aadhaar_score > pan_score and aadhaar_score >= 4:
        return "Aadhaar"

    # Fallback to direct substring search
    if "INCOME" in text_upper or "PERMANENT ACCOUNT" in text_upper:
        return "PAN"
    if "AADHAAR" in text_upper or "UIDAI" in text_upper:
        return "Aadhaar"

    return "Unknown"