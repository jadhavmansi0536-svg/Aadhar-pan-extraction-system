import os
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment

EXCEL_COLUMNS = [
    "S.No", "Document Type", "Name", "Father's Name", "DOB", "Gender",
    "Aadhaar Number", "PAN Number", "Address", "File Name"
]


def export_to_excel(records, output_path="output/extracted_data.xlsx"):
    """Export extracted records to an Excel file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    dataframe = pd.DataFrame(records)
    for column in EXCEL_COLUMNS:
        if column not in dataframe.columns:
            dataframe[column] = ""
    dataframe = dataframe[EXCEL_COLUMNS]
    dataframe["S.No"] = range(1, len(dataframe) + 1)
    dataframe.to_excel(output_path, index=False)

    workbook = load_workbook(output_path)
    worksheet = workbook.active
    for cell in worksheet[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center")
    for column_cells in worksheet.columns:
        max_length = 0
        for cell in column_cells:
            if cell.value is not None:
                max_length = max(max_length, len(str(cell.value)))
        worksheet.column_dimensions[column_cells[0].column_letter].width = min(max_length + 2, 40)
    worksheet.freeze_panes = "A2"
    worksheet.auto_filter.ref = worksheet.dimensions
    workbook.save(output_path)
    return output_path
