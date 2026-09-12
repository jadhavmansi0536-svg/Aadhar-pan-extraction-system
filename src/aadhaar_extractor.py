import re


def is_aadhaar_header_or_footer(line):
    cleaned = line.upper().strip()
    blacklist = [
        "GOVERNMENT OF INDIA", "GOVT OF INDIA", "GOVT. OF INDIA",
        "BHARAT SARKAR", "UNIQUE IDENTIFICATION AUTHORITY",
        "UIDAI", "ENROLMENT", "MERA AADHAAR", "MERI PEHCHAN",
        "HELP@UIDAI.GOV.IN", "WWW.UIDAI.GOV.IN", "1947",
        "SYNTHETIC DOCUMENT", "SOFTWARE TESTING", "SAMPLE AADHAAR CARD",
        "ELECTRONICALLY GENERATED", "AADHAAR NUMBER", "AADHAAR NO"
    ]
    return any(term in cleaned for term in blacklist)


def is_valid_aadhaar_name(line):
    if not line:
        return False
    cleaned = line.strip()
    if len(re.sub(r"[.\s]", "", cleaned)) < 2:
        return False
    if not re.match(r"^[A-Za-z\s\.]+$", cleaned):
        return False
    if is_aadhaar_header_or_footer(cleaned):
        return False
    if re.search(r"\d", cleaned):
        return False
    if re.search(r"\b(MALE|FEMALE|TRANSGENDER|GENDER|DOB|YEAR|BIRTH)\b", cleaned, re.IGNORECASE):
        return False
    return True


def extract_aadhaar_data(text):
    """
    Extract Aadhaar-related fields from OCR or digital text.
    Handles synthetic samples as well as real Aadhaar cards (unlabeled name, bilingual text).
    """

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    result = {
        "Name": "",
        "DOB": "",
        "Gender": "",
        "Aadhaar Number": "",
        "Address": ""
    }

    # 1. Extract Aadhaar Number (12 digits, spaced or unspaced)
    aadhaar_match = re.search(
        r"\b(\d{4})\s?(\d{4})\s?(\d{4})\b",
        text
    )

    if aadhaar_match:
        result["Aadhaar Number"] = "".join(aadhaar_match.groups())

    # 2. Extract Date of Birth / Year of Birth
    dob_match = re.search(
        r"\b(\d{1,2})[/\-\.](\d{1,2})[/\-\.](\d{4})\b",
        text
    )

    if dob_match:
        d, m, y = dob_match.groups()
        result["DOB"] = f"{int(d):02d}/{int(m):02d}/{y}"
    else:
        # Check for Year of Birth (e.g. YOB: 1980)
        yob_match = re.search(
            r"\b(?:YEAR OF BIRTH|YOB|DOB)[\s:]*(\d{4})\b",
            text,
            re.IGNORECASE
        )
        if yob_match:
            result["DOB"] = yob_match.group(1)

    # 3. Extract Gender
    gender_match = re.search(
        r"\b(MALE|FEMALE|TRANSGENDER)\b",
        text.upper()
    )

    if gender_match:
        result["Gender"] = gender_match.group().title()
    elif "महिला" in text:
        result["Gender"] = "Female"
    elif "पुरुष" in text:
        result["Gender"] = "Male"

    # 4. Extract Name
    # Attempt 1: Explicit "Name:" label (Synthetic and labeled formats)
    for i, line in enumerate(lines):
        if re.search(r"\bNAME\b", line, re.IGNORECASE):
            name = re.sub(
                r".*\bNAME\b\s*:?\s*",
                "",
                line,
                flags=re.IGNORECASE
            ).strip()
            name = re.sub(r"^[\s/:\|\-\.\u0900-\u097F]+", "", name).strip()
            name = re.sub(r"[\s/:\|\-\.\u0900-\u097F]+$", "", name).strip()

            if is_valid_aadhaar_name(name):
                result["Name"] = name
                break
            elif i + 1 < len(lines) and is_valid_aadhaar_name(lines[i + 1]):
                result["Name"] = lines[i + 1]
                break

    # Attempt 2: Real Aadhaar format (unlabeled Name before DOB / Gender)
    if not result["Name"]:
        cutoff_idx = len(lines)
        for i, line in enumerate(lines):
            if re.search(
                r"\b(DOB|DATE OF BIRTH|YEAR OF BIRTH|MALE|FEMALE|लिंग|जन्म)\b",
                line,
                re.IGNORECASE
            ):
                cutoff_idx = i
                break

        # Check candidate lines in reverse from DOB (the closest line immediately before DOB is the English name)
        for line in reversed(lines[:cutoff_idx]):
            cleaned = re.sub(r"^[^A-Za-z]+", "", line).strip()
            words = cleaned.split()
            if len(words) >= 2 and all(w[0].isupper() for w in words) and is_valid_aadhaar_name(cleaned):
                result["Name"] = cleaned
                break

        # Fallback if no multi-word Title Case name found
        if not result["Name"]:
            for line in reversed(lines[:cutoff_idx]):
                cleaned = re.sub(r"^[^A-Za-z]+", "", line).strip()
                if is_valid_aadhaar_name(cleaned):
                    result["Name"] = cleaned
                    break

    # 5. Extract Address
    for i, line in enumerate(lines):
        if re.search(r"\b(?:ADDRESS|पता)\b", line, re.IGNORECASE):
            address_parts = []

            current = re.sub(
                r".*\b(?:ADDRESS|पता)\b\s*:?\s*",
                "",
                line,
                flags=re.IGNORECASE
            ).strip()

            if current:
                address_parts.append(current)

            for next_line in lines[i + 1:]:
                if re.search(
                    r"\b(AADHAAR|DOB|GENDER|MALE|FEMALE|VID|\d{4}\s\d{4})\b",
                    next_line,
                    re.IGNORECASE
                ):
                    break

                if re.search(
                    r"synthetic document|software testing|help@uidai|www\.uidai",
                    next_line,
                    re.IGNORECASE
                ):
                    break

                address_parts.append(next_line)

            result["Address"] = " ".join(address_parts)
            break

    return result