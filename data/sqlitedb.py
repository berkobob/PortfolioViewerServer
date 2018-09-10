"""
29-08-18: Antoine Lever - Portfolio Viewer
          Model implementation and API using sqlite3
          API should contain database methods only and use dicts
"""

import sqlite3
from data.sqlScripts import tables, cols, sql
from flask import flash


class sqlitedb():

    def __init__(self):
        try:
            self.db = sqlite3.connect("data/database.db",
                                      check_same_thread=False)
            self.c = self.db.cursor()
            for table in tables:
                self.c.execute(table)
            self.db.commit()
        except sqlite3.Error as e:
            self.db.rollback()

    def __del__(self):
        self.db.close()

    def new(self, user, port):
        """ Create a new and empty portfolio """
        try:
            self.c.execute(sql['new'], (user, port))
            self.db.commit()
        except sqlite3.Error as e:
            self.db.rollback()
            flash("Can't create new portfolio in db because "+str(e))

    def add(self, stock):
        """ Add a stock to an existing portfolio """
        cols = ', '.join(stock.keys())
        place = ':'+',:'.join(stock.keys())
        add = sql['add'] % (cols, place)

        try:
            self.c.execute(add, stock)
            self.db.commit()
        except sqlite3.Error as e:
            self.db.rollback()
            flash("Can't add stock to db because "+str(e))

    def update_port(self, port):
        """ update port values based on updated stock values """
        cols = ', '.join(port.keys())
        place = ':'+',:'.join(port.keys())
        upd = sql['upd_port'] % (cols, place)

        try:
            self.c.execute(upd, port)
            self.db.commit()
        except sqlite3.Error as e:
            self.db.rollback()
            flash("Can't update port in db because "+str(e))

    def ports(self, user):
        """ Return a list of port dicts """
        try:
            self.c.execute(sql['ports'], (user,))
            ports = self.c.fetchall()
            return [dict(zip(cols['port'], port)) for port in ports]
        except sqlite3.Error as e:
            flash("Can't get ports becuase "+str(e))

    def stocks(self, user, port):
        """ Return a list of stock dicts """
        try:
            self.c.execute(sql['stocks'], (user, port))
            port = self.c.fetchall()
            return [dict(zip(cols['stock'], stock)) for stock in port]
        except sqlite3.Error as e:
            flash("Can't get stocks because "+str(e))

    def del_port(self, user, port):
        """ del a port from ports and stocks tables """
        try:
            self.c.execute(sql['del_port'], (user, port))
            self.c.execute(sql['del_stocks'], (user, port))
            self.db.commit()
        except sqlite3.Error as e:
            self.db.rollback()
            flash("Can't delete port because "+str(e))

    def del_stock(self, port, stock):
        """ del one stock from a port """
        try:
            self.c.execute(sql['del_stock'], (stock['user'], port, stock))
            self.db.commit()
        except sqlite3.Error as e:
            self.db.rollback()
            flash("Can't delete stock because "+str(e))

    def update_stock(self, stock):
        """ update stock values """
        try:
            self.c.execute(sql['upd_stock'], (
                           stock['last'], stock['delta'], stock['percent'],
                           stock['stamp'], stock['user'], stock['port'],
                           stock['name']))
            self.db.commit()
        except Exception as e:
            flash("Can't update stock in db because "+str(e))

    def is_user(self, user):
        try:
            self.c.execute("SELECT * FROM users WHERE\
                            user=?", (user, ))
            return self.c.fetchone()[1]
        except sqlite3.Error as e:
            flash("Database error: "+str(e))
        except Exception as e:
            return False


if __name__ == '__main__':
    db = sqlitedb()
