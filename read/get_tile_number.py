import cv2
import pytesseract
import numpy as np
from PIL import Image

# Path to the Tesseract executable (update this if needed)
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

def get_tile_number(pil_image):
    # Convert PIL image to OpenCV format (numpy array)
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # OCR to detect number
    detected_text = pytesseract.image_to_string(thresh, config='--psm 6 --oem 3 outputbase digits')

    # Filter digits
    numbers = ''.join(filter(str.isdigit, detected_text))

    return numbers


