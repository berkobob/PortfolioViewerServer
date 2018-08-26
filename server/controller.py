from data import data

names = ['port', 'name', 'ticker', 'shares', 'price', 'exchange']
port_headers = ['port', 'positions', 'paid', 'last', 'change', 'total', 'delta', 'percent']

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

    e = data._update_new_port(port)
    return e
    