"""
29-08-18: Antoine Lever - Portfolio Viewer
          SQL Scripts, constants and table column names
"""

stockTable = """ CREATE TABLE IF NOT EXISTS stocks (
    port text NOT NULL,        /* 0 Portfolio name               */
    name text NOT NULL,        /* 1 Stock name                   */
    ticker text NOT NULL,      /* 2 Ticker used for update       */
    shares integer DEFAULT 0,  /* 3 How many shares              */
    price real DEFAULT 0.0,    /* 4 Average purchase price       */
    exchange text NOT NULL,    /* 5 LSE, NASDAQ, etc             */
    last real,                 /* 6 Latest price                 */
    delta real,                /* 7 Today's price change         */
    percent real,              /* 8 Today's price change in %    */
    stamp numeric,             /* 9 Date and time of last update */
    symbol text,               /* 10 GBP, USD, ETC               */
    FOREIGN KEY (port) REFERENCES ports(port),
    PRIMARY KEY (port, name)
    )"""

portTable = """ CREATE TABLE IF NOT EXISTS ports (
    port text PRIMARY KEY,     /* Porfolio name                 */
    positions integer,         /* How many stocks in portfolio  */
    paid real DEFAULT 0.0,     /* How much paid for portfolio   */
    value real DEFAULT 0.0,    /* Current value of port         */
    change real DEFAULT 0.0,   /* Total change in port value    */
    percent real DEFAULT 0.0,  /* Total percent change in port  */
    delta real DEFAULT 0.0,    /* Change in value today         */
    pofpaid real DEFAULT 0.0,  /* Today's percent change v paid */
    pofval real DEFAULT 0.0    /* Percent of value changed      */
    )"""

tables = [portTable, stockTable]

""" Names of the columns in the stocks table """
stock = ['port', 'name', 'ticker', 'shares', 'price', 'exchange', 'last',
         'delta', 'percent', 'stamp', 'symbol']

""" Names of the columns in the ports table """
port = ['port', 'positions', 'paid', 'value', 'change', 'percent', 'delta',
        'pofpaid', 'pofval']

""" Names of columns in raw stocks data to be added"""
raw = ['port', 'ticker', 'shares', 'price', 'exchange']

cols = {"stock": stock, "port": port, "raw": raw}

new = "INSERT OR REPLACE INTO ports(port) values(?)"      # new port
add = "INSERT OR REPLACE INTO stocks(%s) VALUES(%s)"      # add stock
stocks = "SELECT * FROM stocks WHERE port=?"              # get stocks
del_port = "DELETE FROM ports WHERE port=?"               # del port
del_stocks = "DELETE FROM stocks WHERE port=?"            # del stocks
del_stock = "DELETE FROM stocks WHERE port=? AND name=?"  # del stock
upd_stock = """UPDATE stocks SET last=?, delta=?, percent=?, stamp=?
            where port=? AND name=? """                   # upd stock
upd_port = "INSERT OR REPLACE INTO ports(%s) VALUES(%s)"  # upd port
sql = {"new": new, "add": add, "stocks": stocks, "del_port": del_port,
       "del_stocks": del_stocks, "del_stock": del_stock,
       "upd_stock": upd_stock, "upd_port": upd_port}
