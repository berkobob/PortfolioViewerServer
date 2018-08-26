stockTable = """ create table if not exists stocks (
    port text NOT NULL,        /* Which portfolio              */
    name text NOT NULL,        /* Raw ticker name              */
    ticker text NOT NULL,      /* Ticker used for update       */
    shares integer NOT NULL,   /* How many shares              */
    price real NOT NULL,       /* Average purchase price       */
    exchange text NOT NULL,    /* LSE, NASDAQ, etc             */
    last real,                 /* Last price                   */
    delta real,                /* Size of change in price      */
    percent real,              /* Size of change in percent    */
    stamp numeric,             /* Date and time of last update */
    symbol text,               /* GBP, USD, ETC                */
    FOREIGN KEY (port) REFERENCES ports(port),
    PRIMARY KEY (port, name)
    )
"""

portTable = """ create table if not exists ports (
    port text PRIMARY KEY,     /* Which portfolio              */
    positions integer,         /* How many stocks in portfolio */
    paid real DEFAULT 0.0,     /* How much paid for portfolio  */
    last real DEFAULT 0.0,     /* Current value of port        */
    change real DEFAULT 0.0,   /* Total change in port value   */
    total real DEFAULT 0.0,    /* Total percent change in port */
    delta real DEFAULT 0.0,    /* Change in value today        */
    percent real DEFAULT 0.0   /* Percent change today         */
    )
"""

tables = [portTable, stockTable]

