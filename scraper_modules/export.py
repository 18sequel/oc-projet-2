import csv
import os

from tqdm import tqdm


FOLDER_NAME = "categories"


def export(informations):
    """
    Exporte les informations de chaque livres d'une catégorie,
    dans un fichier .csv
    """
    if not os.path.exists(FOLDER_NAME):
        os.mkdir(FOLDER_NAME)
    for category in tqdm(informations,
                         desc='Exporting',
                         unit='ticks',
                         colour='green'):
        with open(f'{FOLDER_NAME}/{category["category_name"]}.csv',
                  "w", encoding="utf-8", newline='') as csv_file:
            csv_writer = csv.writer(csv_file,
                                    delimiter=",",
                                    quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
            headers = True
            if headers:
                csv_writer.writerow(list(category["books"][0].keys()))
                headers = False
            for book in category["books"]:
                csv_writer.writerow(list(book.values()))
