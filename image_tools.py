import requests
import os
from PIL import Image


def download_img(url, filename):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as file:
        file.write(response.content)
    resize_image(filename)


def resize_image(img_src):
    image = Image.open(img_src)
    image.thumbnail((1080, 1080))
    image.save(img_src)
