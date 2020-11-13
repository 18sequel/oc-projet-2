import os

from scraper_modules.export import export
from scraper_modules.scraper import scraper


if __name__ == "__main__":
    categories = scraper()
    export(categories)
    os.system("pause")
