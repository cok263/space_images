import requests
import os
from urllib.parse import urljoin


def download_img(url, filename):
    response = requests.get(url)
    response.raise_for_status()
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as file:
        file.write(response.content)


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
    images = [img['file_url'].replace('//imgsrc.hubblesite.org/hvi','https://media.stsci.edu')
              for img in answer['image_files']]
    img_link = images[-1]
    download_img(img_link, 'images/{}.{}'.format(id, get_extension(img_link)))

def main():
    download_hubble_image(1)
#    fetch_spacex_last_launch(12)
    
    #print(*images, sep='\n')
    

if __name__ == '__main__':
    main()