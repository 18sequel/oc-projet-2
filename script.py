import csv
import requests

from bs4 import BeautifulSoup


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


url = input('url du livre: ')
informations = get_book_informations(url)

with open(f'{informations["title"]}.csv', 'w', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    csv_writer.writerow(list(informations.keys()))
    csv_writer.writerow(list(informations.values()))
