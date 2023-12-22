import cv2
import numpy as np
import os

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def extract_and_save_yellow_regions(image_path, output_folder):
    create_directory_if_not_exists(output_folder)
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    lower_yellow = np.array([150, 150, 0], dtype=np.uint8)
    upper_yellow = np.array([255, 255, 50], dtype=np.uint8)
    mask_yellow = cv2.inRange(image_rgb, lower_yellow, upper_yellow)
    kernel = np.ones((3,3), np.uint8)
    mask_closed = cv2.morphologyEx(mask_yellow, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(mask_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    region_file_paths = []

    lower_red = np.array([200, 0, 0], dtype=np.uint8)
    upper_red = np.array([255, 100, 100], dtype=np.uint8)

    for i, contour in enumerate(contours):
        mask = np.zeros_like(mask_yellow)
        cv2.drawContours(mask, [contour], -1, color=255, thickness=cv2.FILLED)
        region = cv2.bitwise_and(image_rgb, image_rgb, mask=mask)

        red_color_mask = cv2.inRange(region, lower_red, upper_red)
        red_color_present = cv2.countNonZero(red_color_mask) > 0

        if red_color_present:
            region_filename = f"{output_folder}/region_{i}.png"
            cv2.imwrite(region_filename, cv2.cvtColor(region, cv2.COLOR_RGB2BGR))
            region_file_paths.append(region_filename)
    
    return region_file_paths

# Usage
image_path = './pics/test.jpeg'
output_folder = './regions_output'
region_file_paths = extract_and_save_yellow_regions(image_path, output_folder)
