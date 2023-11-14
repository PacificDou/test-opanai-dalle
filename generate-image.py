from openai import OpenAI
import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


client = OpenAI()

response = client.images.generate(
  model="dall-e-3",
  prompt="a white siamese cat",
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url
print(image_url)


output_image_path = 'data/generate-image-000.jpg'
resp = requests.get(image_url)
with open('data/generate-image-000.jpg', 'wb') as f:
    f.write(resp.content)


img = mpimg.imread(output_image_path)
imgplot = plt.imshow(img)
plt.show()


