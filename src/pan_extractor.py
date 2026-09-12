import re
from datetime import datetime


def is_blacklisted(line):
    """
    Check if a line is a known government header, card label, or disclaimer.
    """
    cleaned = line.upper().strip()
    exact_blacklist = {
        "INCOME TAX DEPARTMENT", "INCOMETAX DEPARTMENT", "TAX DEPARTMENT",
        "GOVT. OF INDIA", "GOVT OF INDIA", "GOVERNMENT OF INDIA",
        "BHARAT SARKAR", "GOVERNMENT",
        "PERMANENT ACCOUNT NUMBER CARD", "PERMANENT ACCOUNT NUMBER",
        "ACCOUNT NUMBER CARD", "ACCOUNT NUMBER",
        "SIGNATURE", "SIGN",
        "DATE OF BIRTH", "DOB",
        "FATHER'S NAME", "FATHERS NAME", "FATHER NAME",
        "NAME", "HOLDER'S NAME", "HOLDERS NAME",
        "SAMPLE", "SAMPLE PAN CARD", "SAMPLE AADHAAR CARD"
    }
    if cleaned in exact_blacklist:
        return True

    blacklist_phrases = [
        "INCOME TAX", "TAX DEPARTMENT",
        "GOVT. OF INDIA", "GOVT OF INDIA", "GOVERNMENT OF INDIA",
        "PERMANENT ACCOUNT NUMBER", "ACCOUNT NUMBER CARD",
        "DATE OF BIRTH", "FATHER'S NAME", "FATHERS NAME",
        "SYNTHETIC DOCUMENT", "SOFTWARE TESTING",
        "UNIQUE IDENTIFICATION", "MERA AADHAAR"
    ]
    for phrase in blacklist_phrases:
        if phrase in cleaned:
            return True

    return False



def sanitize_name_str(s):
    """
    Clean OCR artifacts from person names (e.g., 'MANS! JADHAV' -> 'MANSI JADHAV').
    """
    if not s:
        return ""
    # Fix ! or | or 1 that looks like I inside or at the end of words
    cleaned = re.sub(r'(?<=[A-Za-z])[!|1](?=[\s\b]|$|[A-Za-z])', 'I', s)
    # Remove everything except English letters, spaces, and periods
    cleaned = re.sub(r'[^A-Za-z\s\.]', '', cleaned).strip()
    # Normalize multiple spaces
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned


def is_valid_name(line):
    """
    Check if a line looks like a valid person's name:
    - Only English letters, spaces, dots
    - No digits
    - Between 3 and 50 characters
    - At least 3 letters
    - Not in blacklist
    """
    if not line:
        return False

    cleaned = line.strip()
    letters_only = re.sub(r"[^A-Za-z]", "", cleaned)
    if len(letters_only) < 3:
        return False

    # Check if mostly English alphabets
    if not re.match(r"^[A-Za-z\s\.]+$", cleaned):
        return False

    if is_blacklisted(cleaned):
        return False

    # Must not match PAN or date patterns
    if re.search(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", cleaned):
        return False
    if re.search(r"\d", cleaned):
        return False

    # Avoid common OCR gibberish (e.g. mixed case single word like 'OOo')
    words = cleaned.split()
    if len(words) == 1 and re.match(r"^[A-Z]{2,}[a-z]+$", words[0]):
        return False

    return True


def clean_label_value(line, label_pattern):
    """
    Removes label prefixes, bilingual markers (Hindi, slashes, colons),
    and returns whatever valid name text remains on the same line.
    If the line contains '/' or '|' (bilingual label header), the name is on the next line.
    """
    if "/" in line or "|" in line:
        return ""

    val = re.sub(label_pattern, "", line, flags=re.IGNORECASE).strip()
    val = re.sub(r"^[\s/:\|\-\.\u0900-\u097F]+", "", val).strip()
    val = re.sub(r"[\s/:\|\-\.\u0900-\u097F]+$", "", val).strip()

    val = sanitize_name_str(val)

    if is_valid_name(val):
        return val
    return ""


def clean_pan_number(candidate):
    """
    Normalize a candidate 10-char string into a valid PAN number format,
    correcting standard OCR character confusions.
    """
    cand = candidate.upper().strip()
    cand = re.sub(r"[\s\-_]", "", cand)
    if len(cand) != 10:
        return None

    c1_5 = cand[:5]
    c6_9 = cand[5:9]
    c10 = cand[9]

    # Map for letters: 0->O, 1->I, 8->B, 5->S, 2->Z
    to_letter = {'0': 'O', '1': 'I', '8': 'B', '5': 'S', '2': 'Z'}
    # Map for digits: O->0, I->1, L->1, B->8, S->5, Z->2, G->6
    to_digit = {'O': '0', 'I': '1', 'L': '1', 'B': '8', 'S': '5', 'Z': '2', 'G': '6'}

    fixed_1_5 = "".join(to_letter.get(ch, ch) for ch in c1_5)
    fixed_6_9 = "".join(to_digit.get(ch, ch) for ch in c6_9)
    fixed_10 = to_letter.get(c10, c10)

    result = fixed_1_5 + fixed_6_9 + fixed_10
    if re.fullmatch(r"[A-Z]{5}[0-9]{4}[A-Z]", result):
        return result
    return None


def extract_pan_data(text):
    """
    Extract PAN-related fields from OCR or digital text.
    Handles synthetic samples, classic unlabeled cards, and modern bilingual cards.
    """
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    result = {
        "Name": "",
        "Father's Name": "",
        "DOB": "",
        "PAN Number": ""
    }

    # ---------------------------------------------------------
    # 1. PAN Number
    # ---------------------------------------------------------
    pan_match = re.search(
        r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
        text.upper()
    )

    if pan_match:
        result["PAN Number"] = pan_match.group()
    else:
        # Check spaced / hyphenated candidates or with character confusion
        candidates = re.findall(
            r"\b[A-Z0-9]{5}[\s\-_]?[A-Z0-9]{4}[\s\-_]?[A-Z0-9]\b",
            text.upper()
        )
        for cand in candidates:
            cleaned = clean_pan_number(cand)
            if cleaned:
                result["PAN Number"] = cleaned
                break

    # ---------------------------------------------------------
    # 2. Date of Birth
    # ---------------------------------------------------------
    dob_match = re.search(
        r"\b(\d{1,2})[/\-\.](\d{1,2})[/\-\.](\d{4})\b",
        text
    )

    if dob_match:
        day, month, year = dob_match.groups()
        result["DOB"] = f"{int(day):02d}/{int(month):02d}/{year}"
    else:
        # Check OCR errors with letter 'O' for '0'
        dob_fuzzy = re.search(
            r"\b([0-9O]{1,2})[/\-\.]([0-9O]{1,2})[/\-\.]([0-9]{4})\b",
            text.upper()
        )
        if dob_fuzzy:
            d_str = dob_fuzzy.group(1).replace("O", "0")
            m_str = dob_fuzzy.group(2).replace("O", "0")
            y_str = dob_fuzzy.group(3)
            try:
                result["DOB"] = f"{int(d_str):02d}/{int(m_str):02d}/{y_str}"
            except ValueError:
                pass

    # ---------------------------------------------------------
    # 3. Name and Father's Name
    # ---------------------------------------------------------
    name_label_regex = r"(?:(?:^|[\s/|])(?:NAME|HOLDER'?S?\s+NAME|नाम)[\s/:\-|]*(?:नाम|NAME)?)"
    father_label_regex = r"(?:(?:^|[\s/|])(?:FATHER'?S?\s+NAME|FATHERS\s+NAME|FATHER\s+NAME|पिता\s*का\s*नाम)[\s/:\-|]*(?:पिता\s*का\s*नाम|FATHER'?S?\s+NAME)?)"

    name_found = False
    father_found = False

    # Attempt 1: Labeled format (New cards & Samples)
    for i, line in enumerate(lines):
        # Match Father's Name label first
        if not father_found and re.search(father_label_regex, line, re.IGNORECASE):
            father_val = clean_label_value(line, father_label_regex)
            if father_val:
                result["Father's Name"] = father_val
                father_found = True
            else:
                for next_line in lines[i + 1:i + 4]:
                    cleaned_next = (
                        clean_label_value(next_line, father_label_regex)
                        if re.search(father_label_regex, next_line, re.IGNORECASE)
                        else sanitize_name_str(next_line)
                    )
                    if is_valid_name(cleaned_next):
                        result["Father's Name"] = cleaned_next
                        father_found = True
                        break

        # Match Holder Name label
        elif not name_found and re.search(name_label_regex, line, re.IGNORECASE):
            if not re.search(r"FATHER|ACCOUNT|INCOME|DEPARTMENT", line, re.IGNORECASE):
                name_val = clean_label_value(line, name_label_regex)
                if name_val:
                    result["Name"] = name_val
                    name_found = True
                else:
                    for next_line in lines[i + 1:i + 4]:
                        if re.search(father_label_regex, next_line, re.IGNORECASE):
                            break
                        cleaned_next = (
                            clean_label_value(next_line, name_label_regex)
                            if re.search(name_label_regex, next_line, re.IGNORECASE)
                            else sanitize_name_str(next_line)
                        )
                        if is_valid_name(cleaned_next):
                            result["Name"] = cleaned_next
                            name_found = True
                            break

    # Attempt 2: Classic Unlabeled format (Old cards without labels)
    if not result["Name"] or not result["Father's Name"]:
        header_idx = -1
        for i, line in enumerate(lines):
            line_up = line.upper()
            if any(term in line_up for term in ["GOVT", "INDIA", "INCOME TAX", "DEPARTMENT", "भारत"]):
                header_idx = max(header_idx, i)

        search_start = header_idx + 1 if header_idx != -1 else 0
        candidate_names = []
        for line in lines[search_start:]:
            line_clean = line.strip()
            if result["PAN Number"] and result["PAN Number"] in line_clean.upper():
                continue
            if re.search(r"\b\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{4}\b", line_clean):
                continue
            if re.search(r"\b(NAME|FATHER|DOB|DATE|BIRTH|YEAR|SIGNATURE|PERMANENT|ACCOUNT)\b", line_clean, re.IGNORECASE):
                continue
            sanitized = sanitize_name_str(line_clean)
            if is_valid_name(sanitized):
                candidate_names.append(sanitized)

        if not result["Name"] and len(candidate_names) >= 1:
            result["Name"] = candidate_names[0]
            if not result["Father's Name"] and len(candidate_names) >= 2:
                result["Father's Name"] = candidate_names[1]
        elif not result["Father's Name"] and len(candidate_names) >= 2:
            if candidate_names[0] != result["Name"]:
                result["Father's Name"] = candidate_names[0]
            else:
                result["Father's Name"] = candidate_names[1]

    return result