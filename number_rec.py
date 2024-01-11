import keras_ocr
import cv2
import numpy as np

def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    threshold_image = cv2.adaptiveThreshold(
        blur_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    bgr_image = cv2.cvtColor(threshold_image, cv2.COLOR_GRAY2BGR)
    return bgr_image

# image_path = 'containers/old_train/containers/container_0.png'
# image_path = 'pics/container_test.png'
image_path = 'pics/test.png'
preprocessed_image = preprocess_image(image_path)
image_for_ocr = keras_ocr.tools.read(preprocessed_image)

pipeline = keras_ocr.pipeline.Pipeline()
predictions = pipeline.recognize([image_for_ocr])[0]

detected_numbers = [] 

for text, box in predictions:
    if text.isdigit(): 
        detected_numbers.append(text) 
        print(f'Detected number: {text}')
        box = box.astype(int)
        cv2.polylines(preprocessed_image, [box], isClosed=True, color=(0, 255, 0), thickness=2)

output_path = 'pics/output_image.jpg' 
cv2.imwrite(output_path, preprocessed_image)

print("Detected numbers:", detected_numbers) 