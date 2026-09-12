# Aadhaar and PAN Card Data Extraction and Excel Generation System

A modern, offline Graphical User Interface (GUI) application built with Python, CustomTkinter, OpenCV, PyMuPDF, and Tesseract OCR to automatically extract personal data from Indian Aadhaar Cards and PAN Cards (Images & PDFs) and export structured results to Excel.

---

##  Key Features

- **Multi-Format Document Upload**: Supports `.jpg`, `.jpeg`, `.png`, and `.pdf` files.
- **Batch Processing**: Upload and extract multiple documents simultaneously.
- **Automatic Document Identification**: Automatically detects whether a document is an **Aadhaar Card** or a **PAN Card** using intelligent keyword scoring and pattern matching.
- **Robust Field Extraction**:
  - **PAN Card**: Name, Father's Name, Date of Birth (DOB), PAN Number (`ABCDE1234F`).
  - **Aadhaar Card**: Name, Date of Birth (DOB), Gender, Aadhaar Number (`12-digit`), Address.
- **Support for Diverse Layouts & Formats**:
  - **Classic Unlabeled PAN Cards**: Uses layout heuristics to detect Holder Name and Father's Name even when labels like `Name:` are missing.
  - **Modern Bilingual Cards**: Handles dual-language labels (`नाम / Name`, `पिता का नाम / Father's Name`) cleanly.
  - **Smartphone Photo Support**: Auto-orients camera photos respecting EXIF metadata.
  - **Digital PDF Parsing**: Extracts text directly from e-PAN / e-Aadhaar vector PDFs without OCR degradation.
  - **OCR Typos & Character Correction**: Auto-corrects common OCR character confusions in numbers and names (e.g. `0` vs `O`, `1` vs `I`).
- **Data Validation & Privacy**:
  - 100% **Local / Offline Processing** (no cloud API, ensuring privacy for sensitive PII data).
  - **Aadhaar Masking**: Aadhaar numbers are masked by default (`XXXX XXXX 1234`) with a toggle to view full numbers.
  - Regex validation for PAN format, Aadhaar format, and DOB format.
- **Interactive GUI**:
  - Document image/page preview.
  - Live data table with manual edit/correction capabilities.
  - One-click export to Excel (`.xlsx`).

---

##  Project Structure

```
Aadhar-pan-extraction-system/
├── main.py                     # Main application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation & execution guide
├── sample_documents/           # Synthetic sample documents for testing
│   ├── create_samples.py       # Script to generate sample cards
│   ├── sample_aadhaar.png
│   ├── sample_aadhaar.pdf
│   ├── sample_pan.png
│   └── sample_pan.pdf
├── output/                     # Generated Excel files output folder
│   └── extracted_data.xlsx
└── src/                        # Source code package
    ├── __init__.py
    ├── gui.py                  # CustomTkinter GUI interface & application logic
    ├── image_processor.py     # Image loading, EXIF orientation & preprocessing
    ├── ocr_processor.py        # Tesseract OCR engine integration (multi-pass)
    ├── pdf_processor.py        # PDF text extraction & image rendering (PyMuPDF)
    ├── document_identifier.py # Document classification engine (Aadhaar vs PAN)
    ├── pan_extractor.py       # PAN card field extraction & layout parsing
    ├── aadhaar_extractor.py   # Aadhaar card field extraction & layout parsing
    ├── validator.py           # Format validation & Aadhaar masking functions
    └── excel_exporter.py      # Pandas & OpenPyXL Excel export module
```

---

##  Technology Stack

- **Language**: Python 3.10+
- **GUI Framework**: `CustomTkinter`, `Tkinter`
- **Computer Vision & Image Processing**: `OpenCV (cv2)`, `Pillow (PIL)`
- **PDF Engine**: `PyMuPDF (fitz)`
- **OCR Engine**: `Tesseract OCR` (via `pytesseract`)
- **Data & Excel Handling**: `Pandas`, `OpenPyXL`

---

##  Installation & Setup

### 1. Prerequisites
- **Python 3.10 or higher**: Download from [python.org](https://www.python.org/).
- **Tesseract OCR**:
  - **Windows**: Download installer from [UB-Mannheim Tesseract Wiki](https://github.com/UB-Mannheim/tesseract/wiki) and install to default location (`C:\Program Files\Tesseract-OCR\tesseract.exe`).

### 2. Install Dependencies
Open terminal or PowerShell in the project directory and run:

```powershell
pip install -r requirements.txt
```

---

##  How to Run the Application

Launch the application using Python:

```powershell
python main.py
```

### Step-by-Step Usage Guide:
1. **Upload Documents**: Click **"Upload Documents"** and select one or more image (`.png`, `.jpg`, `.jpeg`) or PDF files.
2. **Extract Data**: Click **"Extract Data"** to automatically process the uploaded files.
3. **Review & Edit**:
   - Select any row in the table to view the document preview.
   - Use the bottom edit panel to manually correct any field if needed.
   - Toggle **"Show Full Aadhaar"** to unmask Aadhaar numbers if required.
4. **Export to Excel**: Click **"Export Excel"** to save the structured output to `output/extracted_data.xlsx`.

---

## 🔒 Security & Privacy Compliance

This system processes all documents **locally on the user's computer**. No document images or extracted data are uploaded to any external server or third-party cloud service. Aadhaar numbers are automatically masked as required by Indian privacy guidelines.
