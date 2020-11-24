import requests
from bs4 import BeautifulSoup


def get_categories():
    """
    Scrape toutes les catégories du site web http://books.toscrape.com/
    """
    categories = []
    url = "http://books.toscrape.com/index.html"
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, "lxml")
        sub_categories = soup.find("ul",
                                   {"class": "nav nav-list"}).li.findAll("li")
        for category in sub_categories:
            category_name = category.a.text.split()[0]
            category_url = f'http://books.toscrape.com/{category.a["href"]}'
            categories.append({category_name: category_url})
        return categories
    else:
        print('get_categories: erreur, "response status-code != 200"')
