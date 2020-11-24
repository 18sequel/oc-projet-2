from threading import Thread

from tqdm import tqdm

from .download_image import download_image
from .get_book_informations import get_book_informations
from .get_books import get_books
from .get_categories import get_categories


def scraper():
    """
    Créer la liste "categories" qui contient :
        - le nom de la catégorie
        - l'url de la catégorie
        - la liste des dictionnaires d'informations de chaque livres
    Lance le téléchargement de l'image de chaque livres
    """
    threads = []
    categories = []
    for category in tqdm(get_categories(),
                         desc='Scrapping/Downloading',
                         unit='ticks',
                         colour='yellow'):
        for category_name, category_url in category.items():
            category = {"category_name": category_name,
                        "category_url": category_url,
                        "books": []}
            for book in get_books(category_url):
                informations = get_book_informations(book)
                category["books"].append(informations)
                download = Thread(
                    target=download_image,
                    args=(informations["image_url"],
                          informations["universal_product_code"],))
                download.start()
                threads.append(download)
            categories.append(category)
    for thread in threads:
        thread.join()
    return categories
