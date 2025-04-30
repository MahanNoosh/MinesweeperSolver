import cv2
import pytesseract
import numpy as np
from PIL import Image

# Path to the Tesseract executable (update this if needed)
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

def get_tile_number(pil_image):
    # Load and preprocess image
    image = np.array(pil_image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Threshold to isolate digits
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Resize for better OCR
    resized = cv2.resize(thresh, (100, 100), interpolation=cv2.INTER_LINEAR)

    # OCR with digit whitelist
    config = "--psm 10 -c tessedit_char_whitelist=12345678"
    text = pytesseract.image_to_string(resized, config=config)

    # Extract and return digit
    number = ''.join(filter(str.isdigit, text))
    print(number)
    return number