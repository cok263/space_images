import requests
import os
from urllib.parse import urljoin
from PIL import Image
from instabot import Bot
from dotenv import load_dotenv


def download_img(url, filename):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as file:
        file.write(response.content)
    resize_image(filename)


def fetch_spacex_launch(launch_num=-1):
    url = 'https://api.spacexdata.com/v4/launches/'
    if launch_num == -1:
        url = urljoin(url, 'latest')
    response = requests.get(url)
    response.raise_for_status()
    launches = response.json()
    launch = launches
    if launch_num is not -1:
        launch = launches[launch_num]
    images = launch['links']['flickr']['original']
    for number, image_link in enumerate(images):
        download_img(image_link, 'images/spacex{}.jpg'.format(number))


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


def resize_image(img_src):
    image = Image.open(img_src)
    image.thumbnail((1080, 1080))
    image.save(img_src)


def upload_to_instagram(login, password, images_dir):
    bot = Bot()
    bot.login(username=login, password=password)
    images = os.listdir(images_dir)
    for image in images:
        bot.upload_photo(os.path.join(images_dir, image), caption="Nice pic!")


def main():
    load_dotenv()
    login = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')
    spacex_launch_id = 12
    fetch_spacex_launch(spacex_launch_id)
    download_hubble_image_collection()
    #upload_to_instagram(login, password, 'images')


if __name__ == '__main__':
    main()
