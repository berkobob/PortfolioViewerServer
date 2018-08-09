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
            self.c.execute("INSERT INTO ports values (?, 0.0, 0.0)", (port,))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            return e

    def add(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

 
if __name__ == '__main__':
    sqlitedb()