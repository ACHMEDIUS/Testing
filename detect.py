import cv2
import numpy as np
import os

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

color_sets = {
    'default': {
        'agrarish': ([225, 230, 200], [240, 250, 220]),
        'bedrijf': ([170, 85, 200], [190, 105, 220]),
        'bos': ([90, 160, 40], [110, 180, 50]),
        'centrum': ([245, 190, 180], [255, 210, 200]),
        'cultuur': ([245, 55, 120], [255, 65, 140]),
        'detailhandel': ([255, 150, 140], [255, 170, 160]),
        'dienstverlening': ([230, 135, 180], [250, 155, 200]),
        'gemengd': ([255, 180, 125], [255, 200, 145]),
        'groen': ([35, 200, 65], [45, 200, 75]),
        'horeca': ([255, 100, 35], [255, 110, 40]),
        'kantoor': ([230, 195, 210], [240, 200, 220]),
        'maatschappelijk': ([0, 150, 150], [50, 255, 255]),
        'natuur': ([0, 100, 0], [50, 255, 50]),
        'overig': ([0, 0, 0], [50, 50, 50]),
        'recreatie': ([0, 150, 150], [50, 255, 255]),
        'sport': ([0, 150, 150], [50, 255, 255]),
        'tuin': ([0, 100, 0], [50, 255, 50]),
        'verkeer': ([0, 0, 150], [50, 50, 255]),
        'water': ([170, 195, 200], [50, 50, 255]),
        'wonen': ([200, 200, 0], [255, 255, 100]),
    },
    'set1': {
        'agrarish': ([225, 230, 200], [240, 250, 220]),
        'bedrijf': ([170, 85, 200], [190, 105, 220]),
        'bos': ([90, 160, 40], [110, 180, 50]),
        'centrum': ([245, 190, 180], [255, 210, 200]),
        'cultuur': ([245, 55, 120], [255, 65, 140]),
        'detailhandel': ([255, 150, 140], [255, 170, 160]),
        'dienstverlening': ([230, 135, 180], [250, 155, 200]),
        'gemengd': ([255, 180, 125], [255, 200, 145]),
        'groen': ([35, 200, 65], [45, 200, 75]),
        'horeca': ([255, 100, 35], [255, 110, 40]),
        'kantoor': ([230, 195, 210], [240, 200, 220]),
        'maatschappelijk': ([0, 150, 150], [50, 255, 255]),
        'natuur': ([0, 100, 0], [50, 255, 50]),
        'overig': ([0, 0, 0], [50, 50, 50]),
        'recreatie': ([0, 150, 150], [50, 255, 255]),
        'sport': ([0, 150, 150], [50, 255, 255]),
        'tuin': ([0, 100, 0], [50, 255, 50]),
        'verkeer': ([0, 0, 150], [50, 50, 255]),
        'water': ([170, 195, 200], [50, 50, 255]),
        'wonen': ([200, 200, 0], [255, 255, 100]),
    },
}

 detect_building_with_red_dot(image_rgb, color_ranges, output_folder=None):
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
                    region_filename = f"{output_folder}/regi
def detect_building_in_middle(image_rgb, color_ranges, output_folder=None):
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
                    region_filename = f"{output_folder}/region_{color_label}_middle.png"
                    cv2.imwrite(region_filename, cv2.cvtColor(region, cv2.COLOR_RGB2BGR))

                label_counts[color_label] = 1
                return label_counts

    return label_counts

def process_image(image_path, color_set='default', output_folder=None):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    color_ranges = color_sets.get(color_set, color_sets['default'])

    label_counts = detect_building_with_red_dot(image_rgb, color_ranges, output_folder)

    if not label_counts:  # If no red dot is found
        label_counts = detect_building_in_middle(image_rgb, color_ranges, output_folder)

    if label_counts:
        max_color_label = max(label_counts, key=label_counts.get)
        print(f"De bestemming is {max_color_label}")
    else:
        print("Geen bestemming gevonden")

def detect_containers(image_path):
    image = cv2.imread(image_path, 0)  
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=50, param2=30, minRadius=10, maxRadius=100)

    # Draw detected circles
    if circles is not None:
        circles = np.round(circles[0, :]).astype(int)
        for (x, y, r) in circles:
            cv2.circle(image, (x, y), r, (0, 255, 0), 2)