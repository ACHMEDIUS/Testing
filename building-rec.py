import cv2
import numpy as np

def highlight_specific_color(image_path, target_color, output_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image from BGR to RGB (OpenCV uses BGR by default)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Define the lower and upper bounds for the target color (in RGB)
    lower_bound = np.array(target_color, dtype=np.uint8)
    upper_bound = np.array(target_color, dtype=np.uint8)

    # Create a binary mask for pixels within the specified color range
    mask = cv2.inRange(image_rgb, lower_bound, upper_bound)

    # Bitwise AND operation to extract the region of interest
    result = cv2.bitwise_and(image, image, mask=mask)

    # Save or display the result
    cv2.imwrite(output_path, cv2.cvtColor(result, cv2.COLOR_BGR2RGB))

# Example usage
image_path = 'destination_map.jpeg'
target_color = [255, 255, 1]  # RGB values for #ff543f
output_path = 'output.jpg'

highlight_specific_color(image_path, target_color, output_path)
