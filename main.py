import requests
import os
from urllib.parse import urljoin
from PIL import Image
from instabot import Bot
from dotenv import load_dotenv


def download_img(url, filename):
    response = requests.get(url)
    response.raise_for_status()
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as file:
        file.write(response.content)
    resizeImage(filename)


def fetch_spacex_last_launch(launch_num=-1):
    url = 'https://api.spacexdata.com/v4/launches/'
    if launch_num == -1:
        url = urljoin(url, 'latest')
    response = requests.get(url)
    response.raise_for_status()
    answer = response.json()
    if launch_num is not -1:
        answer = answer[launch_num]
    images = answer['links']['flickr']['original']
    for number, image_link in enumerate(images):
        download_img(image_link, 'images/spacex{}.jpg'.format(number))


def get_extension(url):
    return url.split('/')[-1].split('.')[-1]


def download_hubble_image(id):
    url = 'http://hubblesite.org/api/v3/image/{}'.format(id)
    response = requests.get(url)
    response.raise_for_status()
    answer = response.json()
    images = [img['file_url'].replace(
        '//imgsrc.hubblesite.org/hvi', 'https://media.stsci.edu'
        ) for img in answer['image_files']]
    img_link = images[-1]
    download_img(img_link, 'images/{}.{}'.format(id, get_extension(img_link)))


def download_hubble_image_collection():
    payload = {
        'page': 'all',
        'collection_name': 'wallpaper',
    }

    url = 'http://hubblesite.org/api/v3/images/'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    answer = response.json()
    images_id = [info['id'] for info in answer]
    for id in images_id:
        print('downloading image id={}...'.format(id))
        download_hubble_image(id)


def resizeImage(img_src):
    image = Image.open(img_src)
    image.thumbnail((1080, 1080))
    image.save(img_src)


def upload_to_instagram(login, password, images_dir):
    bot = Bot()
    bot.login(username=login, password=password)
    images_list = os.listdir(images_dir)
    for image in images_list:
        bot.upload_photo(os.path.join(images_dir, image), caption="Nice pic!")


def main():
    load_dotenv()
    login = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')
    fetch_spacex_last_launch(12)
    download_hubble_image_collection()
    upload_to_instagram(login, password, 'images')


if __name__ == '__main__':
    main()
