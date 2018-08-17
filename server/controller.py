from data import data

names = ['port', 'name', 'ticker', 'shares', 'price', 'exchange']

def load_port(port, stocks):
    print(f'loading port {port}')
    for stock in stocks:
        stock.insert(0, port)
        stock = dict(zip(names, stock))
        print(stock)

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
    return e