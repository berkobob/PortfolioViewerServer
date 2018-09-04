"""
29-08-18: Antoine Lever - Portfolio Viewer
          SQL Scripts, constants and table column names
"""

stockTable = """ CREATE TABLE IF NOT EXISTS stocks (
    user text NOT NULL,        /* 0 Username of this user        */
    port text NOT NULL,        /* 1 Portfolio name               */
    name text NOT NULL,        /* 2 Stock name                   */
    ticker text NOT NULL,      /* 3 Ticker used for update       */
    shares integer DEFAULT 0,  /* 4 How many shares              */
    price real DEFAULT 0.0,    /* 5 Average purchase price       */
    exchange text NOT NULL,    /* 6 LSE, NASDAQ, etc             */
    last real,                 /* 7 Latest price                 */
    delta real,                /* 8 Today's price change         */
    percent real,              /* 9 Today's price change in %    */
    stamp numeric,             /* 10 Date and time of last update */
    symbol text,               /* 11 GBP, USD, ETC               */
    FOREIGN KEY (port) REFERENCES ports(port),
    PRIMARY KEY (user, port, name)
    )"""

portTable = """ CREATE TABLE IF NOT EXISTS ports (
    user text,                 /* User name of this user        */ 
    port text,                 /* Porfolio name                 */
    positions integer,         /* How many stocks in portfolio  */
    paid real DEFAULT 0.0,     /* How much paid for portfolio   */
    value real DEFAULT 0.0,    /* Current value of port         */
    change real DEFAULT 0.0,   /* Total change in port value    */
    percent real DEFAULT 0.0,  /* Total percent change in port  */
    delta real DEFAULT 0.0,    /* Change in value today         */
    pofpaid real DEFAULT 0.0,  /* Today's percent change v paid */
    pofval real DEFAULT 0.0,   /* Percent of value changed      */
    PRIMARY KEY (user, port)
    )"""

userTable = """ CREATE TABLE IF NOT EXISTS users (
    user text PRIMARY KEY,     /* User name of this user        */
    password text              /* Password for this user        */
    )"""

tables = [portTable, stockTable, userTable]

# Names of the columns in the stocks table
stock = ['user', 'port', 'name', 'ticker', 'shares', 'price', 'exchange',
         'last', 'delta', 'percent', 'stamp', 'symbol']

# Names of the columns in the ports table
port = ['user', 'port', 'positions', 'paid', 'value', 'change', 'percent',
        'delta', 'pofpaid', 'pofval']

# Names of columns in raw stocks data to be added
raw = ['port', 'ticker', 'shares', 'price', 'exchange']

cols = {"stock": stock, "port": port, "raw": raw}

new = "INSERT OR REPLACE INTO ports(user, port) values(?, ?)"        # n port
add = "INSERT OR REPLACE INTO stocks(%s) VALUES(%s)"                 # a stock
stocks = "SELECT * FROM stocks WHERE user=? AND port=?"              # g stocks
del_port = "DELETE FROM ports WHERE user=? AND port=?"               # d port
del_stocks = "DELETE FROM stocks WHERE user=? AND  port=?"           # d stocks
del_stock = "DELETE FROM stocks WHERE user=? AND port=? AND name=?"  # d stock
upd_stock = "UPDATE stocks SET last=?, delta=?, percent=?, stamp=? \
            where user=? AND port=? AND name=?"                      # u stock
upd_port = "INSERT OR REPLACE INTO ports(%s) VALUES(%s)"             # u port
sql = {"new": new, "add": add, "stocks": stocks, "del_port": del_port,
       "del_stocks": del_stocks, "del_stock": del_stock,
       "upd_stock": upd_stock, "upd_port": upd_port}
