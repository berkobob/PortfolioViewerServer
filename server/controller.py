from data import data
from server.pricing import update_price
import re

names = ['port', 'name', 'ticker', 'shares', 'price', 'exchange']
port_headers = ['port', 'positions', 'paid', 'last', 'change', 'total', 'delta', 'percent']
stock_headers = ['port', 'name', 'ticker', 'shares', 'price', 'exchange', 'last', 'delta', 
                 'percent', 'stamp', 'symbol']

def ports():
    e = data.ports()
    if not isinstance(e, list):
        return e

    ports = [dict(zip(port_headers, port)) for port in e]

    for port in ports:
        port['paid'] = '{:0,.0f}'.format(port['paid'])

    return ports

def add_stock(stock):
    stock['name'] = stock['ticker']
    stock['last'] = "0.0"
    stock['delta'] = "0.0"
    stock['percent'] = "0.0"
    stock['stamp'] = 'NONE'
    stock['symbol'] = '$'

    if stock['ticker'][-1] != '.':
        if '.' in stock['ticker']:
            stock['ticker'] = stock['ticker'].replace('.','-')
        if 'LSE' in stock['exchange'    ]:
            stock['ticker'] = stock['ticker']+"."
        
    if 'LSE' in stock['exchange']:
        stock['ticker'] = stock['ticker']+"L"
        stock['symbol'] = "£"

    e = data.add(stock)
    if e:
        return e

    e = data._update_new_port(stock['port'])
    return e

def load_port(port, f):
    try:
        with open(f) as file:
            file.readline()  # discard header row
            for row in file:
                stock = row.rstrip('\n').split(',')
                stock.insert(0, port)
                stock = dict(zip(['port', 'ticker', 'shares', 'price', 'exchange'], stock))
                e = add_stock(stock)
    except Exception as e:
        print("controller: ", str(e))
        return e

    e = data.new(port)
    if e:
        return e

    e = update(port)
    if e:
        return e

    e = data._update_new_port(port)
    return e
    
def update(port):
    stocks = data.stocks(port)
    if not isinstance(stocks, list):
        return stocks

    msg=[]

    for stock in stocks:
        ticker = dict(zip(stock_headers, stock))
        ticker = update_price(ticker)
        e = data.update_stock(ticker)
        if e:
            msg.append(e)

def get_port(port):
    port =  data.stocks(port)
    if not isinstance(port, list):
        return(port)

    port = [dict(zip(stock_headers, stock)) for stock in port]
    
    for stock in port:
        stock['shares'] = '{:,d}'.format(stock['shares'])
        stock['price'] = '{}{:0,.2f}'.format(stock['symbol'], stock['price'])  # price
        stock['last'] = '{}{:0,.2f}'.format(stock['symbol'], stock['last'])  # last
        stock['delta'] = '{}{:0,.2f}'.format(stock['symbol'], stock['delta'])  # delta
        stock['percent'] = '{:0,.2f}%'.format(stock['percent'])  # percent
        get_time = re.compile("\d{1,2}:\d{2}[A-Z]{2}\s[A-Z]{3}") 
        try:
            stock['stamp'] = get_time.findall(stock['stamp'])[0]
        except Exception as e:
            stock['stamp'] = "No update"

    return(port)
    