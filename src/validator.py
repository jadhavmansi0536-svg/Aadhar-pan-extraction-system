import re
from datetime import datetime


def validate_aadhaar(aadhaar_number):
    """
    Validate Aadhaar number format.
    """

    cleaned = re.sub(r"\s+", "", aadhaar_number)

    return bool(
        re.fullmatch(r"\d{12}", cleaned)
    )


def validate_pan(pan_number):
    """
    Validate PAN number format.
    """

    return bool(
        re.fullmatch(
            r"[A-Z]{5}[0-9]{4}[A-Z]",
            pan_number.upper()
        )
    )


def validate_dob(dob):
    """
    Validate date of birth in DD/MM/YYYY format.
    """

    if not dob:
        return False

    try:
        datetime.strptime(dob, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def mask_aadhaar(aadhaar_number):
    """
    Mask Aadhaar number and show only the last four digits.
    """

    cleaned = re.sub(r"\s+", "", aadhaar_number)

    if len(cleaned) == 12 and cleaned.isdigit():
        return "XXXX XXXX " + cleaned[-4:]

    return aadhaar_number