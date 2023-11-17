import os
import requests
import base64


API_KEY = os.environ.get('API_KEY', 'UNKNOWN')

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')



image_path = 'data/dog.png'
mask_path = 'data/dog.png.mask.png'
image_base64 = encode_image(image_path)
mask_base64 = encode_image(mask_path)


#----- caption image
url = 'http://127.0.0.1:5001/roboflow-staging/us-central1/light-v2-api/caption-image?api_key=' + API_KEY
params = { 'image': image_base64 }
headers = { 'Content-Type': 'application/json' }
resp = requests.post(url, headers=headers, json=params)
if resp.status_code == 200:
  print(resp.json())
else:
  print(resp.status_code)
  print(resp.content.decode('utf-8'))



#----- synthetic image
url = 'http://127.0.0.1:5001/roboflow-staging/us-central1/light-v2-api/synthetic-image?api_key=' + API_KEY
params = { 'image': image_base64 }
headers = { 'Content-Type': 'application/json' }
resp = requests.post(url, headers=headers, json=params)
if resp.status_code == 200:
  print(resp.json())
else:
  print(resp.status_code)
  print(resp.content.decode('utf-8'))




#----- edit image
url = 'http://127.0.0.1:5001/roboflow-staging/us-central1/light-v2-api/edit-image?api_key=' + API_KEY
params = { 'image': image_base64, 'mask': mask_base64, 
          'prompt': '''The image shows a playful cat in the midst of a lush green lawn or field. The cat has a tan coat with a white belly and a darker mask-like marking around its eyes, giving it an endearing expression. Its ears are pricked up and it has a bushy tail that curves upwards with a darker tip, which may hint at its breed characteristics, but without a full view or more information, specific breed identification is not precise.

          The cat is interacting with a classic black and white paneled soccer ball, appearing to be either pushing it with its nose or preparing to bite it. The size of the soccer ball relative to the cat suggests that the cat is quite young, probably just a few months old, given that the soccer ball looks almost as large as the pup.
          ''' }
headers = { 'Content-Type': 'application/json' }
resp = requests.post(url, headers=headers, json=params)
if resp.status_code == 200:
  print(resp.json())
else:
  print(resp.status_code)
  print(resp.content.decode('utf-8'))



