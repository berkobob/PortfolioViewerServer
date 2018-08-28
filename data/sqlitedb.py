import sqlite3
from sqlite3 import Error
from data.sqlScripts import tables

class sqlitedb():

    def __init__(self):
        try:
            self.db = sqlite3.connect("data/database.db", 
                check_same_thread=False)
            self.c = self.db.cursor()
            for table in tables:
                self.c.execute(table)
                self.db.commit()
        except Error as e:
            print(e)
            self.db.rollback()
        
    def __del__(self):
        self.db.close()

    def new(self, port):
        try:
            self.c.execute("INSERT OR REPLACE INTO ports(port) values(?)", (port,))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            return e

    def add(self, stock):
        cols = ', '.join(stock.keys())
        place = ':'+',:'.join(stock.keys())
        sql = "INSERT OR REPLACE INTO stocks(%s) VALUES(%s)" % (cols, place)

        try:
            self.c.execute(sql, stock)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            return e

    def update(self):
        pass

    def ports(self):
        try:
            self.c.execute("SELECT * FROM ports")
            ports = self.c.fetchall()
            return ports
        except Exception as e:
            return e

    def stocks(self, port):
        try:
            self.c.execute("SELECT * FROM stocks WHERE port=?", (port,))
            return(self.c.fetchall())
        except Exception as e:
            return e

    def del_port(self, port):
        try:
            self.c.execute("DELETE FROM ports WHERE port=?", (port,))
            self.c.execute("DELETE FROM stocks WHERE port=?", (port,))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            return e      

    def del_stock(self, port, stock):
        try:
            self.c.execute("DELETE FROM stocks WHERE port=? AND name=?", 
                (port, stock))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            return e

    def _update_new_port(self, port):
        try:
            self.c.execute("SELECT * FROM stocks WHERE port=?",(port,))
            stocks = self.c.fetchall()
        except Exception as e:
            return e

        count = 0
        paid = 0
        last = 0.0
        change = 0.0
        total = 0.0
        percent = 0.0

        for stock in stocks:
            count += 1
            paid += stock[3] * stock[4]
            last += stock[3] * stock[6]
            change += stock[3] * stock[7]
            

        try:
            self.c.execute("UPDATE ports SET positions = ?, paid = ? WHERE port=?",(count, paid, port))
        except Exception as e:
            return e

    def update_stock(self, stock):
        try:
            self.c.execute("""UPDATE stocks SET last=?, delta=?, percent=?, stamp=?
            where port=? AND name=? """,
            (stock['last'], stock['delta'], stock['percent'], stock['stamp'],
             stock['port'], stock['name']))
            self.db.commit()
        except Exception as e:
            return e

if __name__ == '__main__':
    db = sqlitedb()
