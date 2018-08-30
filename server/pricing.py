from bs4 import BeautifulSoup
import requests
from flask import flash


def update_price(stock):
    page = requests.get("https://uk.finance.yahoo.com/quote/"+stock['ticker'])

    soup = BeautifulSoup(page.content, 'html.parser')
    price = soup.find_all('span', class_="Trsdu(0.3s)")

    if price:
        last = price[0].get_text().replace(',', '')
        stock['last'] = float(last)
        if stock['exchange'] == 'LSE':
            stock['last'] /= 100
        delta, percent = price[1].get_text().split(' ')
        stock['delta'] = float(delta)
        if stock['exchange'] == 'LSE':
            stock['delta'] /= 100
        stock['percent'] = float(percent.replace('(', '').replace(')', '')
                                                         .replace('%', ''))
    else:
        msg = "{} failed to update".format(stock['name'])
        flash(msg)

    stamp = soup.find('div', attrs={'id': 'quote-market-notice'})
    if stamp:
        stock['stamp'] = stamp.get_text().replace('  ', ' ')
    else:
        stock['stamp'] = "None"

    print("pricing. Updating:", stock['name'])
    return stock


if __name__ == '__main__':
    updatePrice("IBM")
