import cv2
import numpy as np
import os
from extra.destination_types import color_sets
import io
import base64

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def detect_middle(image_rgb, color_ranges):
    h, w, _ = image_rgb.shape
    mid_x, mid_y = w // 2, h // 2
    output_image = None
    destination_type = None 

    for color_label, (lower, upper) in color_ranges.items():
        mask_color = cv2.inRange(image_rgb, np.array(lower), np.array(upper))
        kernel = np.ones((3, 3), np.uint8)
        mask_closed_color = cv2.morphologyEx(mask_color, cv2.MORPH_CLOSE, kernel)
        contours_color, _ = cv2.findContours(mask_closed_color, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours_color:
            if cv2.pointPolygonTest(contour, (mid_x, mid_y), False) >= 0:
                mask = np.zeros_like(mask_color)
                cv2.drawContours(mask, [contour], -1, color=255, thickness=cv2.FILLED)
                region = cv2.bitwise_and(image_rgb, image_rgb, mask=mask)
                output_image = process_image(region, color_label)
                destination_type = color_label  
                print(f"Destination type: {destination_type}")  
                break  
    
    return output_image


def process_image(region, color_label):
    gray = cv2.cvtColor(region, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=80,
                               param1=100, param2=40, minRadius=20, maxRadius=90)

    if circles is not None:
        circles = np.round(circles[0, :]).astype(int)
        for (x, y, r) in circles:
            cv2.circle(region, (x, y), r, (0, 255, 0), 4)

    return cv2.cvtColor(region, cv2.COLOR_RGB2BGR)

def process_middle(image_path, color_set='default', save_output=False, output_folder=None):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    color_ranges = color_sets.get(color_set, color_sets['default'])
    processed_image = detect_middle(image_rgb, color_ranges)

    if save_output and processed_image is not None:
        if output_folder:
            create_directory_if_not_exists(output_folder)
            output_path = os.path.join(output_folder, 'processed_output.png')
            cv2.imwrite(output_path, processed_image)

    return processed_image