# Aadhaar & PAN Data Extraction System

A desktop GUI application that extracts Aadhaar and PAN card information from images and PDF documents using OCR, identifies the document type, validates extracted fields, allows manual corrections, and exports the results to Excel.

## Features

- Upload one or multiple Aadhaar/PAN documents
- Supports JPG, JPEG, PNG and PDF files
- Converts PDF pages into images for processing
- Image preprocessing with OpenCV
- OCR text extraction using Tesseract OCR
- Automatic Aadhaar/PAN document identification
- Aadhaar extraction: Name, DOB, Gender, Aadhaar Number and Address
- PAN extraction: Name, Father's Name, DOB and PAN Number
- Format validation for Aadhaar, PAN and DOB
- Aadhaar masking by default for safer display
- Manual correction of extracted data before export
- Batch processing of multiple documents
- Excel export with Pandas and OpenPyXL
- Synthetic sample documents for testing

## Technology Stack

- Python 3
- CustomTkinter / Tkinter - desktop GUI
- OpenCV - image preprocessing
- Tesseract OCR / pytesseract - OCR text extraction
- PyMuPDF - PDF processing
- Regular Expressions - document identification and field extraction
- Pandas - tabular data handling
- OpenPyXL - Excel formatting
- Pillow - sample document generation and image handling

## Project Structure

```text
Aadhar-pan-extraction-system/
├── main.py
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
│   ├── gui.py
│   ├── image_processor.py
│   ├── ocr_processor.py
│   ├── pdf_processor.py
│   ├── document_identifier.py
│   ├── aadhaar_extractor.py
│   ├── pan_extractor.py
│   ├── validator.py
│   └── excel_exporter.py
├── sample_documents/
│   └── create_samples.py
└── output/
    └── extracted_data.xlsx
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/jadhavmansi0536-svg/Aadhar-pan-extraction-system.git
cd Aadhar-pan-extraction-system
```

### 2. Create and activate a virtual environment

Windows CMD:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install Tesseract OCR

Install Tesseract OCR separately on Windows. The application checks the system PATH and also supports the standard Windows installation path:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

## Generate Sample Documents

From the project root:

```bash
python sample_documents\create_samples.py
```

This creates synthetic Aadhaar and PAN PNG/PDF documents for software testing. These are not real identity documents.

## Run the Application

```bash
python main.py
```

### Typical workflow

1. Click **Upload Documents**.
2. Select one or more supported image/PDF files.
3. Click **Extract Data**.
4. Review the detected document type and extracted fields.
5. Select a row to preview/edit the extracted values.
6. Use **Save Correction** if a value needs correction.
7. Click **Export Excel** to generate `output/extracted_data.xlsx`.

## Excel Output

The exported workbook contains these columns:

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

## Validation and Privacy

Aadhaar and PAN values are checked against their expected formats. Aadhaar numbers are masked in the GUI by default and can be shown in full only when the user explicitly enables the option.

For real identity documents, use the application only in an authorized and secure environment. The included sample documents are synthetic test data.

## Notes

OCR accuracy depends on image quality, document layout, orientation, and text clarity. The extraction rules are designed for the supplied formats and common layouts, but OCR results should always be reviewed before using the exported data.

## Author

Mansi Jadhav
