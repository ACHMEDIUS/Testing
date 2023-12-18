import cv2
import numpy as np

def highlight_and_fill_yellow_regions(image_path, output_path):
    # Read the image
    image = cv2.imread(image_path)
    original_shape = image.shape  # Save the original shape for later
    
    # Convert to the RGB color space
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Define a color range for yellow, allowing for some variation
    lower_yellow = np.array([150, 150, 0], dtype=np.uint8)
    upper_yellow = np.array([255, 255, 50], dtype=np.uint8)
    
    # Create a mask for yellow color
    mask_yellow = cv2.inRange(image_rgb, lower_yellow, upper_yellow)
    
    # Use morphological operations to close gaps - dilation followed by erosion
    kernel = np.ones((3,3), np.uint8)
    mask_closed = cv2.morphologyEx(mask_yellow, cv2.MORPH_CLOSE, kernel)
    
    # Find contours in the mask and fill them
    contours, _ = cv2.findContours(mask_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask_filled = cv2.drawContours(mask_closed.copy(), contours, -1, (255), thickness=cv2.FILLED)
    
    # Bitwise-AND mask and original image
    result = cv2.bitwise_and(image_rgb, image_rgb, mask=mask_filled)
    
    # Convert the result to BGR before saving
    result_bgr = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
    
    # Ensure the resolution matches the original image
    if result_bgr.shape != original_shape:
        result_brg = cv2.resize(result_bgr, (original_shape[1], original_shape[0]), interpolation=cv2.INTER_AREA)
    
    # Save the result
    cv2.imwrite(output_path, result_bgr)

# Usage example
image_path = './pics/test.jpeg'  # Replace with the path to your input image
output_path = 'output.png'  # Replace with the path to save the output image

# Run the function
highlight_and_fill_yellow_regions(image_path, output_path)
