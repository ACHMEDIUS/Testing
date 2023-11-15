import base64
import requests
import tkinter as tk
from tkinter import filedialog

# OpenAI API Key
api_key = "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"

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
# image_path = r"C:\Users\Behrad\Documents\GitHub\Testing\test.jpeg"
image_path = filedialog.askopenfilename(initialdir="/", title="Select Image", filetypes=(("JPEG files", "*.jpeg"), ("PNG files", "*.png")))

# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Prompt text that the user can set
prompt_text = input("Enter the prompt text: ")

payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": prompt_text
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


# Create a tkinter window
root = tk.Tk()

# Function to get the file path of the selected image


# Create a button to select the image
select_button = tk.Button(root, text="Select Drawing", command=image_path)
select_button.pack()

# Run the tkinter window
root.mainloop()


print(response.json())