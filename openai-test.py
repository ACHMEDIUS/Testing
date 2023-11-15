import base64
import requests

# OpenAI API Key
api_key = "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"

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = r"C:\Users\Behrad\Documents\GitHub\Testing\test.jpeg"

# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# verander prompt naar op base van gebouw en niet cirkel in de bouwtekekning

payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "Van het roodgemaarkeerde gebied wat is de bestemming?, wat zijn de goot- en bouwhoogtes? De goot- en bouwhoogtes kun je vinden binnen de bestemming, dit zijn 2 getallen. Geef je reactie als volgt: Goothoogte: x meter Bouwhoogte: y meter Bestemming: z en indien je het niet kunt lezen mag je x y en z leeglaten en geef geen extra uitleg" 
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}", 
              "detail": "high"
            }
          }
        ]
      }
    ],
    "max_tokens": 300
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)



print(response.json())