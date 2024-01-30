from detect_module import process_middle
import base64
import requests
import cv2
import re

image_path = "pics/map.jpeg"
output_path = "output"
color_set = 'set1'
save_output = True

# Troubleshooting: Confirm the image path and processing parameters
print(f"Processing image: {image_path} with color_set: {color_set}, save_output: {save_output}, output_path: {output_path}")

try:
    processed_image = process_middle(image_path, color_set, save_output, output_path)
    if processed_image is None:
        raise ValueError("Processed image is None. Image processing failed.")
except Exception as e:
    print(f"Error during image processing: {e}")
    exit()

# Convert to base64
try:
    _, buffer = cv2.imencode('.jpg', processed_image)
    base64_image = base64.b64encode(buffer).decode('utf-8')
except Exception as e:
    print(f"Error during image conversion to base64: {e}")
    exit()

# OpenAI key
api_key = ""

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "As your response, give me just the number(s) in green marked circle part of the image (all the numbers)"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                        "detail": "low"
                    }
                }
            ]
        }
    ],
    "max_tokens": 300
}

try:
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    if response.status_code == 200:
        numbers_string = response.json()['choices'][0]['message']['content']
        numbers = re.findall(r'\d+', numbers_string)
        numbers = [int(num) for num in numbers[:2]]  # Convert strings to integers

        # Enforce order and handle different cases
        if len(numbers) == 0:
            print("No numbers detected in the image.")
        elif len(numbers) == 1:
            print(f"Detected number: {numbers[0]}")
        else:
            print(f"Detected numbers: {numbers}")
    else:
        print(f"Error in OpenAI API call: {response.status_code}, {response.text}")
except Exception as e:
    print(f"Exception during OpenAI API call: {e}")