import os
import cv2
import customtkinter as ctk

from tkinter import filedialog, messagebox, ttk
from PIL import Image

from src.image_processor import preprocess_image
from src.ocr_processor import extract_text
from src.pdf_processor import pdf_to_images
from src.document_identifier import identify_document
from src.aadhaar_extractor import extract_aadhaar_data
from src.pan_extractor import extract_pan_data
from src.validator import (
    validate_aadhaar,
    validate_pan,
    validate_dob,
    mask_aadhaar
)
from src.excel_exporter import export_to_excel


class ExtractionApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Aadhaar & PAN Data Extraction System")
        self.root.geometry("1250x700")
        self.root.minsize(1100, 650)

        self.files = []
        self.records = []
        self.preview_image = None

        self.create_interface()

    # =========================================================
    # CREATE INTERFACE
    # =========================================================

    def create_interface(self):

        title = ctk.CTkLabel(
            self.root,
            text="Aadhaar & PAN Data Extraction System",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=(4, 2))

        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=2)

        ctk.CTkButton(button_frame, text="Upload Documents", command=self.upload_files, width=140, height=32).grid(row=0, column=0, padx=5)
        ctk.CTkButton(button_frame, text="Extract Data", command=self.extract_data, width=140, height=32).grid(row=0, column=1, padx=5)
        ctk.CTkButton(button_frame, text="Clear", command=self.clear_data, width=140, height=32).grid(row=0, column=2, padx=5)
        ctk.CTkButton(button_frame, text="Export Excel", command=self.export_excel, width=140, height=32).grid(row=0, column=3, padx=5)

        self.full_aadhaar_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(button_frame, text="Show Full Aadhaar", variable=self.full_aadhaar_var, command=self.refresh_table).grid(row=0, column=4, padx=8)

        self.status_label = ctk.CTkLabel(self.root, text="Status: Ready", font=("Arial", 13))
        self.status_label.pack(pady=1)

        self.file_label = ctk.CTkLabel(self.root, text="No documents selected", font=("Arial", 12))
        self.file_label.pack(pady=1)

        self.preview_frame = ctk.CTkFrame(self.root, height=145)
        self.preview_frame.pack(fill="x", padx=15, pady=3)
        self.preview_frame.pack_propagate(False)

        self.preview_title = ctk.CTkLabel(self.preview_frame, text="Document Preview", font=("Arial", 15, "bold"))
        self.preview_title.pack(pady=(3, 1))

        self.preview_label = ctk.CTkLabel(self.preview_frame, text="No document selected", width=500, height=110)
        self.preview_label.pack(pady=2)

        table_frame = ctk.CTkFrame(self.root)
        table_frame.pack(fill="both", expand=True, padx=15, pady=3)

        columns = ("S.No", "Document Type", "Name", "Father's Name", "DOB", "Gender", "Aadhaar Number", "PAN Number", "Address", "File Name")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=5)

        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=120, anchor="center")

        widths = {"S.No":55, "Document Type":110, "Name":130, "Father's Name":130, "DOB":100, "Gender":90, "Aadhaar Number":130, "PAN Number":120, "Address":250, "File Name":180}
        for column, width in widths.items():
            self.tree.column(column, width=width)

        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        self.tree.bind("<<TreeviewSelect>>", self.load_selected_row)

        edit_frame = ctk.CTkFrame(self.root)
        edit_frame.pack(fill="x", padx=15, pady=3)
        for column in range(8):
            edit_frame.grid_columnconfigure(column, weight=1)

        ctk.CTkLabel(edit_frame, text="Select a row and edit fields below:", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=8, pady=(3, 2))

        self.edit_entries = {}
        edit_fields = ["Name", "Father's Name", "DOB", "Gender", "Aadhaar Number", "PAN Number", "Address"]
        for index, field in enumerate(edit_fields):
            row = (index // 4) + 1
            column = (index % 4) * 2
            ctk.CTkLabel(edit_frame, text=field).grid(row=row, column=column, padx=4, pady=2)
            entry = ctk.CTkEntry(edit_frame, width=175, height=28)
            entry.grid(row=row, column=column + 1, padx=4, pady=2, sticky="ew")
            self.edit_entries[field] = entry

        ctk.CTkButton(edit_frame, text="Save Correction", command=self.save_correction, width=150, height=30).grid(row=3, column=6, columnspan=2, padx=5, pady=3)

    def upload_files(self):
        file_paths = filedialog.askopenfilenames(
            title="Select Aadhaar/PAN Documents",
            filetypes=[("Supported Files", "*.jpg *.jpeg *.png *.pdf"), ("All Files", "*.*")]
        )
        if not file_paths:
            return
        self.files = list(file_paths)
        self.file_label.configure(text=f"{len(self.files)} document(s) selected")
        self.status_label.configure(text="Status: Documents selected")
        self.show_preview(self.files[0])

    def reset_preview(self, text="No document selected"):
        self.preview_image = None
        self.preview_label.configure(image=None, text=text)

    def show_preview(self, file_path):
        try:
            if file_path.lower().endswith(".pdf"):
                images = pdf_to_images(file_path)
                if not images:
                    self.reset_preview("Unable to preview document")
                    return
                image = images[0]
            else:
                image = cv2.imread(file_path)
            if image is None:
                self.reset_preview("Unable to preview document")
                return
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(image)
            pil_image.thumbnail((700, 105))
            self.preview_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=pil_image.size)
            self.preview_label.configure(image=self.preview_image, text="")
        except Exception as error:
            self.reset_preview(f"Preview unavailable: {error}")

    def process_file(self, file_path):
        if file_path.lower().endswith(".pdf"):
            images = pdf_to_images(file_path)
            if not images:
                raise ValueError("PDF contains no readable pages")
            image = images[0]
        else:
            image = cv2.imread(file_path)
            if image is None:
                raise ValueError("Unable to read image")

        processed = preprocess_image(image)
        text = extract_text(processed)
        document_type = identify_document(text)

        if document_type == "Aadhaar":
            extracted = extract_aadhaar_data(text)
            aadhaar = extracted.get("Aadhaar Number", "")
            if aadhaar and not validate_aadhaar(aadhaar):
                aadhaar = ""
            dob = extracted.get("DOB", "")
            if dob and not validate_dob(dob):
                dob = ""
            record = {
                "Document Type": "Aadhaar",
                "Name": extracted.get("Name", ""),
                "Father's Name": "",
                "DOB": dob,
                "Gender": extracted.get("Gender", ""),
                "Aadhaar Number": aadhaar,
                "PAN Number": "",
                "Address": extracted.get("Address", ""),
                "File Name": os.path.basename(file_path),
                "_file_path": file_path
            }
        elif document_type == "PAN":
            extracted = extract_pan_data(text)
            pan = extracted.get("PAN Number", "")
            if pan and not validate_pan(pan):
                pan = ""
            dob = extracted.get("DOB", "")
            if dob and not validate_dob(dob):
                dob = ""
            record = {
                "Document Type": "PAN",
                "Name": extracted.get("Name", ""),
                "Father's Name": extracted.get("Father's Name", ""),
                "DOB": dob,
                "Gender": "",
                "Aadhaar Number": "",
                "PAN Number": pan,
                "Address": "",
                "File Name": os.path.basename(file_path),
                "_file_path": file_path
            }
        else:
            record = {
                "Document Type": "Unknown", "Name": "", "Father's Name": "", "DOB": "", "Gender": "",
                "Aadhaar Number": "", "PAN Number": "", "Address": "", "File Name": os.path.basename(file_path), "_file_path": file_path
            }
        return record

    def extract_data(self):
        if not self.files:
            messagebox.showwarning("No Files", "Please upload documents first.")
            return
        self.records = []
        for item in self.tree.get_children():
            self.tree.delete(item)
        for file_path in self.files:
            try:
                self.status_label.configure(text=f"Processing: {os.path.basename(file_path)}")
                self.root.update_idletasks()
                self.records.append(self.process_file(file_path))
            except Exception as error:
                messagebox.showerror("Processing Error", f"{os.path.basename(file_path)}\n\n{error}")
        self.refresh_table()
        self.status_label.configure(text=f"Status: Processed {len(self.records)} document(s)")

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for index, record in enumerate(self.records, start=1):
            aadhaar = record["Aadhaar Number"]
            display_aadhaar = mask_aadhaar(aadhaar) if aadhaar and not self.full_aadhaar_var.get() else aadhaar
            values = (index, record["Document Type"], record["Name"], record["Father's Name"], record["DOB"], record["Gender"], display_aadhaar, record["PAN Number"], record["Address"], record["File Name"])
            self.tree.insert("", "end", values=values)

    def load_selected_row(self, event=None):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0])["values"]
        if not values:
            return
        record_index = int(values[0]) - 1
        if 0 <= record_index < len(self.records):
            file_path = self.records[record_index].get("_file_path")
            if file_path and os.path.exists(file_path):
                self.show_preview(file_path)
        fields = ["Name", "Father's Name", "DOB", "Gender", "Aadhaar Number", "PAN Number", "Address"]
        for index, field in enumerate(fields, start=2):
            self.edit_entries[field].delete(0, "end")
            value = str(values[index])
            if field == "Aadhaar Number" and value.startswith("XXXX"):
                value = self.records[record_index]["Aadhaar Number"]
            self.edit_entries[field].insert(0, value)

    def save_correction(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Row Selected", "Please select a row first.")
            return
        row_number = int(self.tree.item(selected[0])["values"][0]) - 1
        for field, entry in self.edit_entries.items():
            self.records[row_number][field] = entry.get().strip()
        self.refresh_table()
        self.status_label.configure(text="Status: Correction saved")

    def export_excel(self):
        if not self.records:
            messagebox.showwarning("No Data", "Please extract data first.")
            return
        records_for_export = []
        for record in self.records:
            record_copy = record.copy()
            if record_copy["Aadhaar Number"] and not self.full_aadhaar_var.get():
                record_copy["Aadhaar Number"] = mask_aadhaar(record_copy["Aadhaar Number"])
            records_for_export.append(record_copy)
        output_path = export_to_excel(records_for_export)
        messagebox.showinfo("Export Successful", f"Excel file created successfully:\n\n{output_path}")
        self.status_label.configure(text="Status: Excel exported successfully")

    def clear_data(self):
        self.files = []
        self.records = []
        for item in self.tree.get_children():
            self.tree.delete(item)
        for entry in self.edit_entries.values():
            entry.delete(0, "end")
        self.reset_preview("No document selected")
        self.file_label.configure(text="No documents selected")
        self.status_label.configure(text="Status: Ready")
        self.root.update_idletasks()


def run_app():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    ExtractionApp(root)
    root.mainloop()
