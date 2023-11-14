from openai import OpenAI
from PIL import Image
import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


client = OpenAI()

image_path = 'data/dog.jpg'


# convert to PNG if necessary
ext = image_path.split('.')[-1]
if ext.lower() != 'png':
    img = Image.open(image_path)
    image_path = image_path[0:-len(ext)] + 'png'
    img.save(image_path)
    print('Convert to png image: {}'.format(image_path))


response = client.images.create_variation(
  image=open(image_path, "rb"),
  n=2,
  size="1024x1024"
)

image_url = response.data[0].url
print(image_url)


output_image_path = image_path + '-variation-000.jpg'
resp = requests.get(image_url)
with open(output_image_path, 'wb') as f:
    f.write(resp.content)


img_org = mpimg.imread(image_path)
img_new = mpimg.imread(output_image_path)

f, axarr = plt.subplots(1,2)
axarr[0].imshow(img_org)
axarr[1].imshow(img_new)
plt.show()


