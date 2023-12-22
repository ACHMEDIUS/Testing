# color_recognition_module.py

import cv2
import numpy as np
import os

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def process_image(image_path, output_folder=None):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Red color range (used for all colors)
    lower_red = np.array([200, 0, 0], dtype=np.uint8)
    upper_red = np.array([255, 100, 100], dtype=np.uint8)

    # Define color ranges for each color you want to recognize
    color_ranges = {
        'agrarish': ([225, 230, 200], [240, 250, 220]), # 235, 240, 210 
        'bedrijf': ([170, 85, 200], [190, 105, 220]), # 180, 95, 210
        'bos': ([90, 160, 40], [110, 180, 50]), # 100, 170, 45
        'centrum': ([245, 190, 180], [255, 210, 200]), # 255, 200, 190
        'cultuur': ([245, 55, 120], [255, 65, 140]), # 255, 60, 130
        'detailhandel': ([255, 150, 140], [255, 170, 160]), # 255, 160, 150
        'dienstverlening': ([230, 135, 180], [250, 155, 200]), # 240, 145, 190
        'gemengd': ([255, 180, 125], [255, 200, 145]), # 255, 190, 135
        'groen': ([35, 200, 65], [45, 200, 75]), # 40, 200, 70
        'horeca': ([255, 100, 35], [255, 110, 40]), # 255, 105, 35
        'kantoor': ([230, 195, 210], [240, 200, 220]), # 235, 195, 215
        'maatschappelijk': ([0, 150, 150], [50, 255, 255]), # 200, 155, 120
        'natuur': ([0, 100, 0], [50, 255, 50]), # 130, 165, 145
        'overig': ([0, 0, 0], [50, 50, 50]), # 235, 225, 235
        'recreatie': ([0, 150, 150], [50, 255, 255]), # 185, 215, 70
        'sport': ([0, 150, 150], [50, 255, 255]), # 130, 200, 70
        'tuin': ([0, 100, 0], [50, 255, 50]), # 200, 215, 110
        'verkeer': ([0, 0, 150], [50, 50, 255]), # 205, 205, 205
        'water': ([170, 195, 200], [50, 50, 255]), # 175, 205, 225
        'wonen': ([200, 200, 0], [255, 255, 100]), # 255, 255, 0 and 255, 255, 180
    }

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
                print(f"De bestemming is {color_label}")

                if output_folder:
                    create_directory_if_not_exists(output_folder)
                    region_filename = f"{output_folder}/region_{color_label}_{i}.png"
                    cv2.imwrite(region_filename, cv2.cvtColor(region, cv2.COLOR_RGB2BGR))
