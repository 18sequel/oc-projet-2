import requests

from bs4 import BeautifulSoup


def get_books(category_url):
    """
    Scrape l'url de chaque livres d'une catégorie via l'url de celle-ci
    """
    books_url = []
    index = 1
    base_url = category_url
    while True:
        if index == 1:
            url = base_url
        else:
            url = base_url.replace("index", f"page-{index}")
        response = requests.get(url)
        if response.ok:
            soup = BeautifulSoup(response.text, "lxml")
            sub_books = soup.find("ol", {"class": "row"}).findAll("li")
            for book in sub_books:
                books_url.append(book.h3.a["href"].replace(
                    "../../../", "http://books.toscrape.com/catalogue/"))
            if soup.find("li", {"class": "next"}):
                index += 1
            else:
                break
        else:
            print('get_books: erreur, "response status-code != 200"')
    return books_url
