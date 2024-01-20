import cv2
import numpy as np
import os
from extra.destination_types import color_sets

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def detect_dot(image_rgb, color_ranges, output_folder=None):
    lower_red = np.array([200, 0, 0], dtype=np.uint8)
    upper_red = np.array([255, 100, 100], dtype=np.uint8)

    for color_label, (lower, upper) in color_ranges.items():
        mask_color = cv2.inRange(image_rgb, np.array(lower), np.array(upper))
        kernel = np.ones((3, 3), np.uint8)
        mask_closed_color = cv2.morphologyEx(mask_color, cv2.MORPH_CLOSE, kernel)
        contours_color, _ = cv2.findContours(mask_closed_color, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours_color:
            mask = np.zeros_like(mask_color)
            cv2.drawContours(mask, [contour], -1, color=255, thickness=cv2.FILLED)
            region = cv2.bitwise_and(image_rgb, image_rgb, mask=mask)

            red_color_mask = cv2.inRange(region, lower_red, upper_red)
            red_color_present = cv2.countNonZero(red_color_mask) > 0

            if red_color_present:
                if output_folder:
                    create_directory_if_not_exists(output_folder)
                    region_filename = f"{output_folder}/region_{color_label}.png"
                    cv2.imwrite(region_filename, cv2.cvtColor(region, cv2.COLOR_RGB2BGR))

                    # Process each region image to detect circles
                    process_image(region_filename, output_folder, f"processed_{color_label}.png")

def detect_middle(image_rgb, color_ranges, output_folder=None):
    h, w, _ = image_rgb.shape
    mid_x, mid_y = w // 2, h // 2

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

                if output_folder:
                    create_directory_if_not_exists(output_folder)
                    region_filename = f"{output_folder}/region_{color_label}.png"
                    cv2.imwrite(region_filename, cv2.cvtColor(region, cv2.COLOR_RGB2BGR))

                    # Process each region image to detect circles
                    process_image(region_filename, output_folder, f"processed_{color_label}.png")

def process_image(image_path, output_directory, output_file_name):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=80,
                               param1=100, param2=40, minRadius=20, maxRadius=90)

    if circles is not None:
        circles = np.round(circles[0, :]).astype(int)
        for (x, y, r) in circles:
            cv2.circle(image, (x, y), r, (0, 255, 0), 4)

    output_path = os.path.join(output_directory, output_file_name)
    cv2.imwrite(output_path, image)

def process_dot(image_path, color_set='default', output_folder=None):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    color_ranges = color_sets.get(color_set, color_sets['default'])
    detect_dot(image_rgb, color_ranges, output_folder)

def process_middle(image_path, color_set='default', output_folder=None):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    color_ranges = color_sets.get(color_set, color_sets['default'])
    detect_middle(image_rgb, color_ranges, output_folder)

