from pix2text import Pix2Text
from typing import Dict
from PIL import Image

# Khởi tạo model Pix2Text khi file được import
p2t = Pix2Text(language="en")  # Hoặc "vi" nếu bạn dùng Pix2Text-Vi

def extract_text_from_image(image_path: str) -> Dict[str, str]:
    """
    Nhận vào đường dẫn ảnh, trả về text OCR & LaTeX (nếu có).
    """
    image = Image.open(image_path)
    result = p2t.recognize(image)

    print("📦 Pix2Text raw output:", type(result), result)  # Gỡ lỗi

    text_result = ""
    latex_result = ""

    if isinstance(result, list):
        # Trường hợp nhiều đoạn kết quả
        text_result = "\n".join([r.get("text", "") for r in result if isinstance(r, dict)])
        latex_result = "\n".join([r.get("latex", "") for r in result if isinstance(r, dict) and "latex" in r])
    elif isinstance(result, dict):
        text_result = result.get("text", "")
        latex_result = result.get("latex", "")
    elif isinstance(result, str):
        # Nếu Pix2Text chỉ trả về chuỗi (không chuẩn), gán vào text
        text_result = result
        latex_result = ""
    else:
        # Trường hợp khác không mong đợi (None, số, v.v.)
        text_result = str(result)
        latex_result = ""

    return {
        "text": text_result,
        "latex": latex_result
    }
