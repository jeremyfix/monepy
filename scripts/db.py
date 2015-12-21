import sqlite3


class DB:
    
    connector = None

    def __init__(self):
        pass

    @staticmethod
    def open(filename):
        DB.connector = sqlite3.connect(filename)

    @staticmethod
    def close():
        DB.connector.close()
        
    @staticmethod
    def do_update(query):
        if DB.connector is not None:
            c = DB.connector.cursor()
            c.execute(query)
            DB.connector.commit()
            return c.lastrowid
        else:
            raise Exception("Not connected to a db")

    @staticmethod
    def do_select(query):
        if DB.connector is not None:
            c = DB.connector.cursor()
            c.execute(query)
            return c.fetchall()
        else:
            raise Exception("Not connected to a db")
