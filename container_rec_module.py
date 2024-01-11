import cv2
import numpy as np
import os

# Function to create a directory if it does not exist
def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def detect_containers(image_path):
    image = cv2.imread(image_path) 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=50, param2=30, minRadius=10, maxRadius=100)

    if circles is not None:
        circles = np.round(circles[0, :]).astype(int)
        for (x, y, r) in circles:
            cv2.circle(image, (x, y), r, (0, 255, 0), 2)


    return image

image_paths = [
    'containers/old_train/containers/container_0.png',
    'containers/old_train/containers/container_1.png',
    'containers/old_train/containers/container_2.png',
    'containers/old_train/containers/container_7.png',
    'containers/old_train/containers/container_8.png',    
]  

output_directory = 'output'
create_directory_if_not_exists(output_directory)

for image_path in image_paths:
    processed_image = detect_containers(image_path)
    output_path = os.path.join(output_directory, os.path.basename(image_path))
    cv2.imwrite(output_path, processed_image)

print("Processing complete. Images saved to:", output_directory)
