import requests
import os
import argparse
from urllib.parse import urljoin
from dotenv import load_dotenv
from PIL import Image

from spacex import fetch_spacex_launch
from hubble import download_hubble_image_collection
from instagram_tools import upload_to_instagram


def create_parser():
    parser = argparse.ArgumentParser(
        description='Программа скачивает космические \
                     фото и загружает в инстаграмм'
    )
    parser.add_argument('--images_dir', help='Папка с фотографиями',
                        default='images')
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    load_dotenv()
    login = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')
    spacex_launch_id = 12
    fetch_spacex_launch(spacex_launch_id, args.images_dir)
    download_hubble_image_collection(args.images_dir)
    upload_to_instagram(login, password, args.images_dir)


if __name__ == '__main__':
    main()
