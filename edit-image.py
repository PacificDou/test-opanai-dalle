from openai import OpenAI
from PIL import Image
import os
import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import ImageDraw


client = OpenAI()

image_path = 'data/cat.jpg'


# convert to PNG if necessary
ext = image_path.split('.')[-1]
if ext.lower() != 'png':
    img = Image.open(image_path)
    image_path = image_path[0:-len(ext)] + 'png'
    img.save(image_path)
    print('Convert to png image: {}'.format(image_path))


# generate mask
mask_image_path = image_path + '.mask.png'
polygon = [(90, 127), (698, 127), (698, 700), (90, 700)] # straight lines between the given coordinates, plus a straight line between the last and the first coordinate
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
  prompt="""This image features a close-up of a fawn or cream-colored cat wearing a cute costume hat that resembles the head of another cat, specifically with features like that of the Hello Kitty character. The hat is predominantly white with black details representing the eyes, whiskers, and six dots above the eyes, which may indicate the presence of eyelashes or maybe a play on the fur pattern typically seen in cartoon character designs. There are also prominent pink details that represent the nose and the inner parts of the ears.

    The cat itself has large, expressive eyes and a small pink nose centered between its short white whiskers. Its facial expression seems relaxed and slightly curious or bemused. The cat's fur appears to be short and well-groomed, and its round face accentuates its endearing look. The background is indistinguishable and somewhat blurred, keeping the focus entirely on the cat.
    """.replace('cat', 'puppy'),
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




