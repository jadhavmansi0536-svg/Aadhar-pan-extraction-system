from PIL import Image, ImageDraw, ImageFont
import os
import pymupdf

OUTPUT_FOLDER = os.path.dirname(__file__)


def get_font(size, bold=False):
    path = r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"
    return ImageFont.truetype(path, size)


def create_aadhaar_sample():
    image = Image.new("RGB", (1600, 1000), "white")
    draw = ImageDraw.Draw(image)
    title_font = get_font(42, True)
    heading_font = get_font(32, True)
    normal_font = get_font(30)
    draw.text((500, 50), "SAMPLE AADHAAR CARD", fill="black", font=title_font)
    draw.text((100, 180), "Name: Mansi Test", fill="black", font=heading_font)
    draw.text((100, 260), "DOB: 15/08/1998", fill="black", font=normal_font)
    draw.text((100, 330), "Gender: FEMALE", fill="black", font=normal_font)
    draw.text((100, 410), "Aadhaar Number: 0000 0000 0000", fill="black", font=heading_font)
    draw.text((100, 520), "Address:", fill="black", font=heading_font)
    draw.text((100, 580), "123 Sample Road, Ahmedabad, Gujarat", fill="black", font=normal_font)
    draw.text((100, 650), "This is a synthetic document for software testing.", fill="black", font=normal_font)
    image_path = os.path.join(OUTPUT_FOLDER, "sample_aadhaar.png")
    image.save(image_path)
    return image_path


def create_pan_sample():
    image = Image.new("RGB", (1600, 1000), "white")
    draw = ImageDraw.Draw(image)
    title_font = get_font(42, True)
    heading_font = get_font(32, True)
    normal_font = get_font(30)
    draw.text((520, 50), "SAMPLE PAN CARD", fill="black", font=title_font)
    draw.text((100, 200), "Name: Mansi Test", fill="black", font=heading_font)
    draw.text((100, 290), "Father's Name: Rajesh Test", fill="black", font=heading_font)
    draw.text((100, 390), "Date of Birth: 15/08/1998", fill="black", font=normal_font)
    draw.text((100, 500), "PAN Number: ABCDE1234F", fill="black", font=heading_font)
    draw.text((100, 620), "This is a synthetic document for software testing.", fill="black", font=normal_font)
    image_path = os.path.join(OUTPUT_FOLDER, "sample_pan.png")
    image.save(image_path)
    return image_path


def create_pdf(image_path, pdf_name):
    pdf_path = os.path.join(OUTPUT_FOLDER, pdf_name)
    image = Image.open(image_path).convert("RGB")
    pdf_document = pymupdf.open()
    page = pdf_document.new_page(width=image.width, height=image.height)
    page.insert_image(page.rect, filename=image_path)
    pdf_document.save(pdf_path)
    pdf_document.close()
    return pdf_path


if __name__ == "__main__":
    aadhaar_image = create_aadhaar_sample()
    pan_image = create_pan_sample()
    create_pdf(aadhaar_image, "sample_aadhaar.pdf")
    create_pdf(pan_image, "sample_pan.pdf")
    print("Sample documents created successfully!")
    print("Aadhaar:", aadhaar_image)
    print("PAN:", pan_image)
