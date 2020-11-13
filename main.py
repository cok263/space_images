import requests
import os
from urllib.parse import urljoin
from dotenv import load_dotenv
from PIL import Image

from spacex import fetch_spacex_launch
from hubble import download_hubble_image_collection
from instagram_tools import upload_to_instagram


def main():
    load_dotenv()
    login = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')
    spacex_launch_id = 12
    fetch_spacex_launch(spacex_launch_id)
    download_hubble_image_collection()
    upload_to_instagram(login, password, 'images')


if __name__ == '__main__':
    main()
