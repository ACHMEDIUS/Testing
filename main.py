from detect_module import process_middle
import base64
import requests
import cv2
import re

image_path = "pics/map.jpeg"
output_path = "output"
color_set = 'set1'
save_output = True
processed_image = process_middle(image_path, color_set, save_output, output_path)

# Convert to base64
_, buffer = cv2.imencode('.jpg', processed_image)
base64_image = base64.b64encode(buffer).decode('utf-8')

# OpenAI key
api_key = "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"

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

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

if response.status_code == 200:
    numbers_string = response.json()['choices'][0]['message']['content']
    numbers = re.findall(r'\d+', numbers_string)
    numbers = [int(num) for num in numbers[:2]] 

    # enforce order
    if len(numbers) == 0:
        print("No height or width detected")
    elif len(numbers) == 1:
        print(f"De bouwhoogte is: {numbers[0]}")
    else:
        print(f"De bouwhoogte is: {numbers[0]}\nDe goothoogte is: {numbers[1]}.")
else:
    print(f"Error: {response.status_code}, {response.text}")