import requests
import os

from image_tools import download_img


def download_hubble_image(id):
    url = 'http://hubblesite.org/api/v3/image/{}'.format(id)
    response = requests.get(url)
    response.raise_for_status()
    image_details = response.json()
    images = [img['file_url'] for img in image_details['image_files']]
    img_link = 'http:{}'.format(images[-1])
    download_img(
        img_link,
        'images/{id}{exp}'.format(id=id, exp=os.path.splitext(img_link)[-1])
    )


def download_hubble_image_collection():
    payload = {
        'page': 'all',
        'collection_name': 'wallpaper',
    }

    url = 'http://hubblesite.org/api/v3/images/'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    images_collection = response.json()
    images_id = [info['id'] for info in images_collection]
    for image_id in images_id:
        print('downloading image id={}...'.format(image_id))
        download_hubble_image(image_id)
