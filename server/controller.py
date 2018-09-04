from data import data, cols
from server.pricing import update_price
from flask import flash
import re


def ports():
    """ Return a list of port dicts with columns formatted """
    ports = data.ports()

    for port in ports:
        port['paid'] = '{:0,.0f}'.format(port['paid'])
        port['value'] = '£{:0,.0f}'.format(port['value'])
        port['change'] = '£{:0,.0f}'.format(port['change'])
        port['percent'] = '{:0,.2f}%'.format(port['percent'])
        port['pofpaid'] = '{:0,.2f}%'.format(port['pofpaid'])
        port['delta'] = '£{:0,.2f}'.format(port['delta'])
        port['pofval'] = '{:0,.2f}%'.format(port['pofval'])

    return ports


def add_stock(stock):
    """ Take raw stock data and create a new stock """
    try:
        stock['shares'] = int(stock['shares'])
    except Exception as e:
        stock['shares'] = 0

    try:
        stock['price'] = float(stock['price'])
    except Exception as e:
        stock['price'] = 0.0

    stock['name'] = stock['ticker']
    stock['last'] = "0.0"
    stock['delta'] = "0.0"
    stock['percent'] = "0.0"
    stock['stamp'] = 'NONE'
    stock['symbol'] = '$'

    if stock['ticker'][-1] != '.':
        if '.' in stock['ticker']:
            stock['ticker'] = stock['ticker'].replace('.', '-')
        if 'LSE' in stock['exchange']:
            stock['ticker'] = stock['ticker']+"."

    if 'LSE' in stock['exchange']:
        stock['ticker'] = stock['ticker']+"L"
        stock['symbol'] = "£"

    data.add(stock)


def load_port(port, f):
    """ import a file of raw stock data and make port full of these stocks """
    try:
        with open(f) as file:
            file.readline()  # discard header row
            for row in file:
                stock = row.rstrip('\n').split(',')
                stock.insert(0, port)
                stock = dict(zip(cols['raw'], stock))
                stock['user'] = session['user']
                add_stock(stock)
    except Exception as e:
        flash("Cannot open file because "+str(e))

    update_stocks(port)


def update_stocks(port):
    """ Update port prices """
    stocks = data.stocks(port)

    for stock in stocks:
        try:
            stock = update_price(stock)
        except Exception as e:
            flash("Could not get price for "+stock['name'])
        data.update_stock(stock)
    update_port(port)


def get_port(port):
    """ Return a formated list of stock dicts """
    port = data.stocks(port)

    for stock in port:
        stock['shares'] = '{:,d}'.format(stock['shares'])
        stock['price'] = '{}{:0,.2f}'.format(stock['symbol'], stock['price'])
        stock['last'] = '{}{:0,.2f}'.format(stock['symbol'], stock['last'])
        stock['delta'] = '{}{:0,.3f}'.format(stock['symbol'], stock['delta'])
        stock['percent'] = '{:0,.2f}%'.format(stock['percent'])
        get_time = re.compile("\d{1,2}:\d{2}[A-Z]{2}\s[A-Z]{3}")
        try:
            stock['stamp'] = get_time.findall(stock['stamp'])[0]
        except Exception as e:
            stock['stamp'] = "No update"

    return(port)


def update_port(port_name):
    stocks = data.stocks(port_name)

    port = {'port': port_name, 'positions': 0, 'paid': 0.0, 'value': 0.0,
            'change': 0.0, 'percent': 0.0, 'delta': 0.0, 'pofpaid': 0.0,
            'pofval': 0.0}

    for stock in stocks:
        port['positions'] += 1
        port['paid'] += stock['shares'] * stock['price']
        port['value'] += stock['shares'] * stock['last']
        port['delta'] += stock['shares'] * stock['delta']

        port['change'] = port['value'] - port['paid']
    try:
        port['percent'] = port['change'] / port['paid'] * 100
        port['pofpaid'] = port['delta'] / port['paid'] * 100
        port['pofval'] = port['delta'] / port['value'] * 100
    except:
        pass

    data.update_port(port)


def is_user(user, password):
    return password == data.is_user(user)
