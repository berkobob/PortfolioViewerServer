from data import data

names = ['port', 'name', 'ticker', 'shares', 'price', 'exchange']

"""
def load_port(port, stocks):
    for stock in stocks:
        stock.insert(0, port)
        stock = dict(zip(names, stock))
"""

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
        return(str(e))

    e = data.new(port)
    
def sort_port(port, col):
    print(f"sorting port {port} on column {col}")