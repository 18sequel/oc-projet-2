import os

import requests


FOLDER_NAME = 'images'

def download_image(image_url, upc):
    """
    Télécharge l'image via l'url
    """

    url = image_url
    response = requests.get(url)

    if response.ok:
        if not os.path.exists(FOLDER_NAME):
            os.mkdir(FOLDER_NAME)

        with open(f'{FOLDER_NAME}/{upc}.png', 'wb') as image:
            image.write(response.content)

    else:
        print('download_image: erreur, "response status-code != 200"')
