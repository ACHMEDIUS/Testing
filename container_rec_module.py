import cv2
import numpy as np
import os

# Function to create a directory if it does not exist
def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def detect_circles(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)  # Adjusted kernel size for GaussianBlur
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=80,
                               param1=100, param2=40, minRadius=20, maxRadius=90)

    if circles is not None:
        circles = np.round(circles[0, :]).astype(int)
        for (x, y, r) in circles:
            cv2.circle(image, (x, y), r, (0, 255, 0), 4)  # Increased thickness for visibility

    return image

def process_image(image_path, output_directory, output_file_name):
    processed_image = detect_circles(image_path)
    output_path = os.path.join(output_directory, output_file_name)
    cv2.imwrite(output_path, processed_image)

# Example usage
image_path = 'pics/output/region_wonen.png'
output_directory = 'pics/output'
output_file_name = 'processed_image.png'

create_directory_if_not_exists(output_directory)
process_image(image_path, output_directory, output_file_name)
