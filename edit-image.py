from openai import OpenAI
from PIL import Image
import os
import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import ImageDraw


client = OpenAI()

image_path = 'data/raccoon.jpg'


# convert to PNG if necessary
ext = image_path.split('.')[-1]
if ext.lower() != 'png':
    img = Image.open(image_path)
    image_path = image_path[0:-len(ext)] + 'png'
    img.save(image_path)
    print('Convert to png image: {}'.format(image_path))


# generate mask
mask_image_path = image_path + '.mask.png'
polygon = [(152, 50), (610, 50), (610, 630), (152, 630)] # straight lines between the given coordinates, plus a straight line between the last and the first coordinate
if not os.path.exists(mask_image_path):
    img = Image.open(image_path)
    mask = Image.new('L', img.size, color=255)
    draw = ImageDraw.Draw(mask)
    draw.polygon(polygon, fill=0)
    img.putalpha(mask)  
    img.save(mask_image_path)
    print('Generate mask: {} {}'.format(mask_image_path, polygon))


response = client.images.edit(
  model="dall-e-2",
  image=open(image_path, "rb"),
  mask=open(mask_image_path, "rb"),
  prompt="""This image features a raccoon perched in a tree. The raccoon's face is visible with its characteristic black mask and pointy ears accentuated by white outlines. 
    Its fur appears dense and mixtures of grey, black, and hints of brown. The creature looks directly at the camera, conveying a sense of curiosity or alertness. 
    The background is slightly blurred, throwing the focus onto the raccoon and allowing us to observe the detail of its fur and the sharpness of its gaze. 
    Surrounding branches suggest the raccoon is nestled comfortably in a green, leafy environment, typical of a woodland or forest habitat where raccoons are often found.""".replace('raccoon', 'cat'),
  n=1,
  size="1024x1024"
)

image_url = response.data[0].url
print(image_url)



output_image_path = image_path + '-edit-000.jpg'
resp = requests.get(image_url)
with open(output_image_path, 'wb') as f:
    f.write(resp.content)


img_org = mpimg.imread(image_path)
img_mask = mpimg.imread(mask_image_path)
img_new = mpimg.imread(output_image_path)

f, axarr = plt.subplots(1, 3)
axarr[0].imshow(img_org)
axarr[1].imshow(img_mask)
axarr[2].imshow(img_new)
plt.show()




