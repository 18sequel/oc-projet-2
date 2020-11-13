from threading import Thread


from tqdm import tqdm


from scraper_modules.get_books import get_books
from scraper_modules.get_categories import get_categories
from scraper_modules.download_image import download_image
from scraper_modules.get_book_informations import get_book_informations


def scraper():
    """
    Créé la liste "categories" qui contient :
        - le nom de la catégorie
        - l'url de la catégorie
        - la liste des dictionnaires d'informations de chaque livres
    Lance le téléchargement de l'image de chaque livres
    """

    threads = []
    categories = []

    for category_name, category_url in tqdm(get_categories().items()):
        category = {}
        category["category_name"] = category_name
        category["category_url"] = category_url
        category["books"] = []

        for book in get_books(category_url):
            informations = get_book_informations(book)
            category["books"].append(informations)
            download = Thread(
                target=download_image,
                args=(
                    informations["image_url"],
                    informations["universal_product_code"],
                ),
            )
            download.start()
            threads.append(download)

        categories.append(category)

    for thread in threads:
        thread.join()

    return categories
