stockTable = """ create table if not exists stocks (
    port text NOT NULL,        /* 0 Which portfolio              */
    name text NOT NULL,        /* 1 Raw ticker name              */
    ticker text NOT NULL,      /* 2 Ticker used for update       */
    shares integer NOT NULL,   /* 3 How many shares              */
    price real NOT NULL,       /* 4 Average purchase price       */
    exchange text NOT NULL,    /* 5 LSE, NASDAQ, etc             */
    last real,                 /* 6 Last price                   */
    delta real,                /* 7 Size of change in price      */
    percent real,              /* 8 Size of change in percent    */
    stamp numeric,             /* 9 Date and time of last update */
    symbol text,               /* 10 GBP, USD, ETC                */
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

