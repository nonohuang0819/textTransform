import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os

# PDF 檔案路徑
pdf_path = 'PDFdata/NTU113-English.pdf'
output_path = 'transformData/transformData.txt'

# 確保輸出目錄存在
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# 打開 PDF 文件
pdf_document = fitz.open(pdf_path)

# 打開輸出文件
with open(output_path, 'w', encoding='utf-8') as output_file:
    # 遍歷每一頁並提取文字
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        text = page.get_text()
        output_file.write(f"Page {page_number + 1}:\n{text}\n")

        # 提取圖片中的文字
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            text_from_image = pytesseract.image_to_string(image, lang='eng')
            output_file.write(f"Text from image {img_index + 1} on page {page_number + 1}:\n{text_from_image}\n")