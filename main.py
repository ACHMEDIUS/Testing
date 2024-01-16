from building_rec_module import process_dot, process_middle
# from container_rec_module import detect_containers
import base64
import requests

image_path = "pics/test.jpeg"
output_folder = 'pics/output'
color_set = 'set1'
# Uncomment the desired processing function
process_dot(image_path, color_set, output_folder)
# process_middle(image_path, color_set, output_folder)

new_image_path = process_dot(image_path, color_set='set1', output_folder=output_folder)

# openai key
api_key = "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"

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Getting the base64 string
base64_image = encode_image(new_image_path)

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
          "text": "Give me just the number(s) in this image"
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

numbers = response.json()['choices'][0]['message']['content']
print(numbers)