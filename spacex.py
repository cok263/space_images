import requests
import os
from urllib.parse import urljoin

from image_tools import download_img


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
