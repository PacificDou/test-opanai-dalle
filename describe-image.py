import base64
from openai import OpenAI

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

image_path = 'data/dog.jpg'
base64_image = encode_image(image_path)


client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4-vision-preview",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "describe this image, provide as many details as possible"},
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          },
        },
      ],
    }
  ],
  max_tokens=300,
)

description = response.choices[0].message.content
print(description)

with open(image_path + '.txt', 'a') as f:
    f.write("--------------------\n{}\n\n\n".format(description))


