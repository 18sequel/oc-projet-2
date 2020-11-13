import os
import csv
from threading import Thread
import json


from tqdm import tqdm


from download_image import download_image
from get_categories import get_categories
from get_books import get_books
from get_book_informations import get_book_informations
from export import export


def scrape():
    threads = []

    categories = []

    for category_name, category_url in tqdm(get_categories().items()):
        category = {}
        category['category_name'] = category_name
        category['category_url'] = category_url
        category['books'] = []

        for book in get_books(category_url):
            informations = get_book_informations(book)
            category['books'].append(informations)

            download = Thread(
                target=download_image, args=(informations['image_url'], informations['universal_product_code'])
            )
            download.start()
            threads.append(download)

        categories.append(category)


    for thread in threads:
        thread.join()

    return categories


if __name__ == '__main__':
    categories = scrape()
    export(categories)
    os.system('pause')
