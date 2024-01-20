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
    label_counts = {}

    for color_label, (lower, upper) in color_ranges.items():
        mask_color = cv2.inRange(image_rgb, np.array(lower), np.array(upper))
        kernel = np.ones((3, 3), np.uint8)
        mask_closed_color = cv2.morphologyEx(mask_color, cv2.MORPH_CLOSE, kernel)
        contours_color, _ = cv2.findContours(mask_closed_color, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for i, contour in enumerate(contours_color):
            mask = np.zeros_like(mask_color)
            cv2.drawContours(mask, [contour], -1, color=255, thickness=cv2.FILLED)
            region = cv2.bitwise_and(image_rgb, image_rgb, mask=mask)

            red_color_mask = cv2.inRange(region, lower_red, upper_red)
            red_color_present = cv2.countNonZero(red_color_mask) > 0

            if red_color_present:
                if color_label in label_counts:
                    label_counts[color_label] += 1
                else:
                    label_counts[color_label] = 1

                if output_folder:
                    create_directory_if_not_exists(output_folder)
                    region_filename = f"{output_folder}/region_{color_label}.png"
                    cv2.imwrite(region_filename, cv2.cvtColor(region, cv2.COLOR_RGB2BGR))

    return label_counts

def detect_middle(image_rgb, color_ranges, output_folder=None):
    h, w, _ = image_rgb.shape
    mid_x, mid_y = w // 2, h // 2
    label_counts = {}

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

                label_counts[color_label] = 1
                return label_counts

    return label_counts

def process_dot(image_path, color_set='default', output_folder=None):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    color_ranges = color_sets.get(color_set, color_sets['default'])

    label_counts = detect_dot(image_rgb, color_ranges, output_folder)

    if label_counts:
        max_color_label = max(label_counts, key=label_counts.get)
        print(f"De bestemming is {max_color_label}")
    else:
        print("Geen bestemming gevonden")

def process_middle(image_path, color_set='default', output_folder=None):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    color_ranges = color_sets.get(color_set, color_sets['default'])

    label_counts = detect_middle(image_rgb, color_ranges, output_folder)

    if label_counts:
        max_color_label = max(label_counts, key=label_counts.get)
        print(f"De bestemming is {max_color_label}")
    else:
        print("Geen bestemming gevonden")


# Testing
image_path = "pics/test.jpeg"
output_folder = 'pics/output'

process_dot(image_path, color_set='set1', output_folder=output_folder)