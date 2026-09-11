import re


def extract_pan_data(text):
    """Extract PAN-related fields from OCR text."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    result = {"Name": "", "Father's Name": "", "DOB": "", "PAN Number": ""}

    pan_match = re.search(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", text.upper())
    if pan_match:
        result["PAN Number"] = pan_match.group()

    dob_match = re.search(r"\b\d{2}[/-]\d{2}[/-]\d{4}\b", text)
    if dob_match:
        result["DOB"] = dob_match.group().replace("-", "/")

    for i, line in enumerate(lines):
        if re.search(r"\bNAME\b", line, re.IGNORECASE):
            name = re.sub(r".*\bNAME\b\s*:?\s*", "", line, flags=re.IGNORECASE).strip()
            if name:
                result["Name"] = name
            elif i + 1 < len(lines):
                result["Name"] = lines[i + 1]
            break

    for i, line in enumerate(lines):
        if re.search(r"FATHER'?S?\s+NAME|FATHERS\s+NAME|FATHER\s+NAME", line, re.IGNORECASE):
            father_name = re.sub(
                r".*(FATHER'?S?\s+NAME|FATHERS\s+NAME|FATHER\s+NAME)\s*:?\s*",
                "", line, flags=re.IGNORECASE
            ).strip()
            if father_name:
                result["Father's Name"] = father_name
            elif i + 1 < len(lines):
                result["Father's Name"] = lines[i + 1]
            break

    return result
