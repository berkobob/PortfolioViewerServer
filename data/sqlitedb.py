import sqlite3
from sqlite3 import Error
from data.sqlScripts import tables

class sqlitedb():

    def __init__(self):
        try:
            self.db = sqlite3.connect("data/database.db", check_same_thread=False)
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
            self.c.execute("INSERT OR REPLACE INTO ports values (?, 0.0, 0.0)", (port,))
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
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            return e
        
        return self.del_stock(port, '*')


    def del_stock(self, port, stock):
        try:
            self.c.execute("DELETE FROM stocks WHERE port=? AND name=?", 
                (port, stock))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            return e

 
if __name__ == '__main__':
    db = sqlitedb()
