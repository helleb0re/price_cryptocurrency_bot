import requests
from bs4 import BeautifulSoup


url = 'https://coinmarketcap.com/'


def start():
    page = requests.get(url)
    data = {}
    soup = BeautifulSoup(page.text, 'html.parser')
    soup1 = soup.find('tbody').find_all('tr', class_="cmc-table-row")[:10]
    for k in soup1:
        a = k.find('td',
                   class_="cmc-table__cell cmc-table__cell--sticky cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--sort-by__name")
        data[a.text] = {}
        b = k.find('td',
                   class_="cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price")
        data[a.text]['price'] = float(b.text[1:].replace(',', ''))
        c = k.find('td',
                   class_="cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__percent-change-24-h")
        data[a.text]['percent_change_24h'] = float(c.text[:-1])
        d = k.find('td',
                   class_="cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__market-cap")
        data[a.text]['market_cap'] = int(d.text[1:].replace(',', ''))
    return data
