import requests
from os.path import splitext

from image_tools import download_img


def download_hubble_image(id, images_dir='images'):
    url = 'http://hubblesite.org/api/v3/image/{}'.format(id)
    response = requests.get(url)
    response.raise_for_status()
    image_details = response.json()
    images = [img['file_url'] for img in image_details['image_files']]
    img_link = 'http:{}'.format(images[-1])
    download_img(
        img_link,
        '{dir}/{id}{exp}'.format(
            dir=images_dir, id=id, exp=splitext(img_link)[-1]
        )
    )


def download_hubble_image_collection(images_dir='images'):
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
        download_hubble_image(image_id, images_dir)
