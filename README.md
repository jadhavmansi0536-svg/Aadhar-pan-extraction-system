# Aadhaar & PAN Data Extraction System

A desktop Python application that extracts Aadhaar and PAN card information from images and PDF documents using OCR, identifies the document type automatically, allows corrections, and exports the final data to Excel.

## Features

- Upload single or multiple JPG, JPEG, PNG, and PDF documents
- Automatic Aadhaar/PAN document identification
- OCR using Tesseract
- OpenCV image preprocessing for OCR
- PDF page conversion using PyMuPDF
- Aadhaar field extraction: Name, DOB, Gender, Aadhaar Number, Address
- PAN field extraction: Name, Father's Name, DOB, PAN Number
- Editable extracted-data table for OCR corrections
- Aadhaar masking in the GUI/export by default
- Batch processing of multiple documents
- Excel export with formatted columns
- Synthetic sample document generator for testing
- Local processing; documents are not sent to a remote OCR service

## Technology Stack

- Python
- CustomTkinter / Tkinter
- OpenCV
- Tesseract OCR / pytesseract
- PyMuPDF
- Regular Expressions
- Pandas
- OpenPyXL
- Pillow

## Project Structure

```text
Aadhar-pan-extraction-system/
├── main.py
├── requirements.txt
├── README.md
├── output/
│   ├── extracted_data.xlsx
│   └── README.md
├── sample_documents/
│   ├── create_samples.py
│   ├── sample_aadhaar.png
│   ├── sample_aadhaar.pdf
│   ├── sample_pan.png
│   └── sample_pan.pdf
└── src/
    ├── __init__.py
    ├── gui.py
    ├── image_processor.py
    ├── ocr_processor.py
    ├── pdf_processor.py
    ├── document_identifier.py
    ├── aadhaar_extractor.py
    ├── pan_extractor.py
    ├── validator.py
    └── excel_exporter.py
```

## Installation

1. Install Python 3.10 or newer.
2. Install Tesseract OCR.
3. Open a terminal in the project folder.
4. Create and activate a virtual environment.
5. Install the Python dependencies:

```bash
pip install -r requirements.txt
```

### Tesseract on Windows

The application automatically looks for Tesseract in PATH and also supports the standard Windows installation path:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

If Tesseract is installed somewhere else, update `TESSERACT_PATH` in `src/ocr_processor.py`.

## Run the Application

From the project root:

```bash
python main.py
```

The GUI workflow is:

```text
Upload Documents
      ↓
Image/PDF Processing
      ↓
Image Enhancement
      ↓
OCR
      ↓
Document Identification
      ↓
Field Extraction
      ↓
Data Validation / Correction
      ↓
Display in Table
      ↓
Export to Excel
```

## Generate Sample Documents

To generate synthetic test documents:

```bash
python sample_documents/create_samples.py
```

The generated sample Aadhaar and PAN image/PDF files are stored in `sample_documents/` and can then be selected from the GUI.

> The sample documents are synthetic test data and are not real identity documents.

## Excel Output

The exported workbook contains:

- S.No
- Document Type
- Name
- Father's Name
- DOB
- Gender
- Aadhaar Number
- PAN Number
- Address
- File Name

The default application output path is:

```text
output/extracted_data.xlsx
```

A sample generated workbook is included in the same `output/` folder.

## Validation and Privacy

PAN numbers are checked against the standard `ABCDE1234F` pattern. Aadhaar numbers are checked for a 12-digit format, and dates are validated using `DD/MM/YYYY` format.

Aadhaar numbers are masked by default so that only the last four digits are displayed/exported unless full Aadhaar display is explicitly enabled in the application.

This project is intended for demonstration and educational use with authorized documents and synthetic samples.

## Author

Mansi Jadhav
