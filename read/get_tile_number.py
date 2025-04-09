import cv2
import pytesseract
from PIL import Image

# Path to the Tesseract executable (update this if needed)
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"


def get_tile_number(image_path):
    # Read the image using OpenCV
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to get a binary image (black and white)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Optionally, apply additional processing like GaussianBlur, dilation, etc.
    # thresh = cv2.GaussianBlur(thresh, (5, 5), 0)

    # Use pytesseract to extract text (numbers) from the processed image
    detected_text = pytesseract.image_to_string(thresh, config='--psm 6 --oem 3 outputbase digits')

    # Extract numbers from the detected text (filter digits)
    numbers = ''.join(filter(str.isdigit, detected_text))

    return numbers
