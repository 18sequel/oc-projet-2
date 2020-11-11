import os
import csv
import time
import requests

from bs4 import BeautifulSoup


def get_categories():
    categories = {}

    url = 'http://books.toscrape.com/index.html'

    response = requests.get(url)

    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')

        sub_categories = soup.find('ul', {'class': 'nav nav-list'}).li.findAll('li')

        for category in sub_categories:
            categories[f'{category.a.text.split()[0]}'] = f'http://books.toscrape.com/{category.a["href"]}'

        return categories

    else:
        print('get_categories: erreur, "response status-code != 200"')


def get_books(category_url):
    books_url = []

    index = 1

    base_url = category_url

    while True:
        if index == 1:
            url = base_url
        else:
            url = base_url.replace('index', f'page-{index}')

        response = requests.get(url)

        if response.ok:
            soup = BeautifulSoup(response.text, 'lxml')

            sub_books = soup.find('ol', {'class': 'row'}).findAll('li')

            for book in sub_books:
                books_url.append(book.h3.a['href'].replace('../../../', 'http://books.toscrape.com/catalogue/'))

            if soup.find('li', {'class': 'next'}):
                index += 1
            else:
                break

        else:
            print('get_books: erreur, "response status-code != 200"')

    return books_url


def get_book_informations(book_url):
    informations = {}

    url = book_url
    informations['product_page_url'] = url

    response = requests.get(url)

    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')

        sub_informations = soup.find('table', {'class': 'table table-striped'}).findAll('tr')

        upc = sub_informations[0].td.text
        informations['universal_ product_code'] = upc

        title = soup.find('div', {'class': 'col-sm-6 product_main'}).h1.text
        informations['title'] = title

        price_incl_tax = sub_informations[3].td.text
        informations['price_including_tax'] = price_incl_tax

        price_excl_tax = sub_informations[2].td.text
        informations['price_excluding_tax'] = price_excl_tax

        number_available = sub_informations[5].td.text
        informations['number_available'] = number_available

        description = soup.find('article', {'class': 'product_page'}).findAll('p')[3].text
        informations['product_description'] = description

        category = soup.find('ul', {'class': 'breadcrumb'}).findAll('li')[2].a.text
        informations['category'] = category

        review_rating = soup.find('div', {'class': 'col-sm-6 product_main'}).findAll('p')[2]['class'][1]
        informations['review_rating'] = review_rating

        image_url = soup.find(
            'div', {'class': 'item active'}
        ).img['src'].replace('../../', 'http://books.toscrape.com/')
        informations['image_url'] = image_url

        return informations

    else:
        print('get_book_informations: erreur, "response status-code != 200"')


def download_image(image_url, upc):
    url = image_url

    response = requests.get(url)

    if response.ok:
        try:
            os.mkdir('images')
        except FileExistsError:
            pass

        with open(f'images/{upc}.png', 'wb') as image:
            image.write(response.content)

    else:
        print('download_image: erreur, "response status-code != 200"')


start_time = time.time()

for category_name, category_url in zip(get_categories().keys(), get_categories().values()):
    try:
        os.mkdir('categories')
    except FileExistsError:
        pass

    with open(f'categories/{category_name}.csv', 'w', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        headers = True

        for book in get_books(category_url):
            informations = get_book_informations(book)

            if headers:
                csv_writer.writerow(list(informations.keys()))
                headers = False

            download_image(informations['image_url'], informations['universal_ product_code'])

            csv_writer.writerow(list(informations.values()))


print(f'Terminé en {time.time() - start_time} secondes.')
os.system('pause')
