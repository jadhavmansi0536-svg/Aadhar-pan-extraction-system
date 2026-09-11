import re


def extract_aadhaar_data(text):
    """Extract Aadhaar-related fields from OCR text."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    result = {"Name": "", "DOB": "", "Gender": "", "Aadhaar Number": "", "Address": ""}

    aadhaar_match = re.search(r"\b\d{4}\s?\d{4}\s?\d{4}\b", text)
    if aadhaar_match:
        result["Aadhaar Number"] = aadhaar_match.group().replace(" ", "")

    dob_match = re.search(r"\b\d{2}[/-]\d{2}[/-]\d{4}\b", text)
    if dob_match:
        result["DOB"] = dob_match.group().replace("-", "/")

    gender_match = re.search(r"\b(MALE|FEMALE|TRANSGENDER)\b", text.upper())
    if gender_match:
        result["Gender"] = gender_match.group().title()

    for i, line in enumerate(lines):
        if re.search(r"\bNAME\b", line, re.IGNORECASE):
            name = re.sub(r".*\bNAME\b\s*:?\s*", "", line, flags=re.IGNORECASE).strip()
            result["Name"] = name or (lines[i + 1] if i + 1 < len(lines) else "")
            break

    for i, line in enumerate(lines):
        if re.search(r"\bADDRESS\b", line, re.IGNORECASE):
            address_parts = []
            current = re.sub(r".*\bADDRESS\b\s*:?\s*", "", line, flags=re.IGNORECASE).strip()
            if current:
                address_parts.append(current)
            for next_line in lines[i + 1:]:
                if re.search(r"\b(AADHAAR|DOB|GENDER|MALE|FEMALE|VID)\b", next_line, re.IGNORECASE):
                    break
                if re.search(r"synthetic document|software testing", next_line, re.IGNORECASE):
                    break
                address_parts.append(next_line)
            result["Address"] = " ".join(address_parts)
            break
    return result
