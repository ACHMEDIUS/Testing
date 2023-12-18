import cv2
import numpy as np
import pytesseract

def preprocess_image(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to segment the digits
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Perform morphological operations to clean the image
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

    return closing

def extract_digits(image):
    # Find contours in the image
    contours, _ = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    digits = []

    # Loop over the contours
    for contour in contours:
        # Get bounding box for each contour
        x, y, w, h = cv2.boundingRect(contour)

        # Extract the region of interest (ROI) containing the digit
        digit_roi = image[y:y + h, x:x + w]

        # Resize the digit ROI to a fixed size (e.g., 28x28) for OCR
        resized_digit = cv2.resize(digit_roi, (28, 28))

        digits.append(resized_digit)

    return digits

def recognize_digits(digits):
    recognized_numbers = []

    for i, digit in enumerate(digits):

        # Convert the digit to text using Tesseract OCR
        number = pytesseract.image_to_string(digit, config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789')

        # Append the recognized number to the list
        recognized_numbers.append(number)

    # Remove newlines and empty strings
    recognized_numbers = [number.replace('\n', '') for number in recognized_numbers if number]

    return recognized_numbers

if __name__ == "__main__":
    image_path = 'Test.png'

    # Preprocess the image
    preprocessed_image = preprocess_image(image_path)

    # Extract individual digits
    digit_rois = extract_digits(preprocessed_image)

    # Recognize the digits
    recognized_numbers = recognize_digits(digit_rois)

    print("Recognized Numbers:", recognized_numbers)
