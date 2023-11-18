from PIL import Image
import pytesseract
import io

def ocr(image_data: bytes):
    try:
        image = Image.open(io.BytesIO(image_data))
        return pytesseract.image_to_string(image)
    except Exception as e:
        return str(e)