from pypdf import PdfReader
from pdf2image import convert_from_path
import pytesseract
import os

pdf_file = "./data/story2.pdf"
output_folder = "./data/images"
text_folder = "./data/text"
os.makedirs(output_folder, exist_ok=True)
os.makedirs(text_folder, exist_ok=True)

# Read pages from PDF file and save to text
pages = convert_from_path(pdf_file, dpi=300, output_folder=output_folder, fmt="jpeg", single_file=False)
pdf_text = []
for i, page in enumerate(pages):
    image_path = os.path.join(output_folder, f"page_{i + 1}.jpg")
    page.save(image_path, "JPEG")
    text = pytesseract.image_to_string(image_path)
    pdf_text.append(text.strip())

print(f"Pages extracted {i}")

# Remove temporary image files
for imgfiles in os.listdir(output_folder):
    img_path = os.path.join(output_folder, imgfiles)
    if os.path.isfile(img_path):
        os.remove(img_path)

print("Writing text to file...")
# Write to text file
output_text_file = "./data/text/extracted_text.txt"
with open(output_text_file, "w", encoding="utf-8") as f:
    f.write("\n\n".join(pdf_text))

print("Text extraction complete.")


