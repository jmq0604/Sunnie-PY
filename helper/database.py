import sqlite3, globals, traceback, sys

from sqlite3 import Error
from helper import sql_tables

class database:
    def __init__(self, database_name="database/database.sqlite"):
        self.__conn = None
        try:
            self.__conn = sqlite3.connect(database_name)
            print("SQLITE Connection Established! v{v}".format(v=sqlite3.version_info))

            for x in globals.sql_commands:
                self.Execute(x)

        except Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    def Connection(self):
        return self.__conn.cursor()

    def CloseConnection(self):
        if self.__conn:
            self.__conn.close()

    def Commit(self):
        self.__conn.commit()

    def Exist(self, table, column, key):
        try:
            sql_statement = """SELECT * FROM {table} WHERE {column} = '{key}'""".format(table=table, column=column, key=key)
    
            c = self.__conn.cursor()
            c.execute(sql_statement)
            rows = c.fetchall()
    
            if not rows:
                return False
            else:
                return True
        except Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    def RetrieveAll(self, table):
        try:
            sql_statement = """SELECT * FROM {table}""".format(table=table)
    
            c = self.__conn.cursor()
            c.execute(sql_statement)
            return c.fetchall()
        except Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    def Retrieve(self, table, column, key, list=False):
        sql_statement = """SELECT * FROM {table} WHERE {column} = '{key}'""".format(table=table, column=column, key=key)

        c = self.__conn.cursor()
        c.execute(sql_statement)
        rows = c.fetchall()

        if not rows:
            self.Insert(table, column, key)
        else:
            if len(rows) == 1 and not list:
                return rows[0]
            return rows

        c.execute(sql_statement)
        rows = c.fetchall()

        if len(rows) == 1 and not list:
            return rows[0]
        return rows

    def Insert(self, table, key, value):
        sql_statement = """INSERT INTO {table}({key}) VALUES('{value}')""".format(table=table,key=key, value=value)

        c = self.__conn.cursor()
        c.execute(sql_statement)

    def Update(self, table, key, value, key_find, colum="id"):
        try:
            sql_statement = """UPDATE {table} SET {key} = '{value}' WHERE {colum} = '{id}';""".format(colum=colum, table=table, key=key, value=value, id=key_find)
    
            c = self.__conn.cursor()
            c.execute(sql_statement)
        except Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    def Deduct(self, table, key, value, key_find, colum="id"):
        try:
            sql_statement = """UPDATE {table} SET {key} = {key} - '{value}' WHERE {colum} = '{id}';""".format(table=table, key=key,
                                                                                                 value=value,
                                                                                                 id=key_find, colum=colum)

            c = self.__conn.cursor()
            c.execute(sql_statement)
        except Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
    
    def Addition(self, table, key, value, key_find, colum="id"):
        try:
            sql_statement = """UPDATE {table} SET {key} = {key} + '{value}' WHERE {colum} = '{id}';""".format(table=table, key=key,
                                                                                                 value=value,
                                                                                                 id=key_find, colum=colum)

            c = self.__conn.cursor()
            c.execute(sql_statement)
        except Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    def Execute(self, command):
        c = self.__conn.cursor()
        c.execute(command)
        return c.fetchall()

    def GetAllTables(self):
        c = self.__conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")

        return_tables = []
        tables = c.fetchall()
        for x in tables:
            return_tables.append(x[0])

        return return_tables

    def GetTableColumn(self, table):
        c = self.__conn.cursor()
        c.execute(f"PRAGMA table_info({table});")

        return_tables = []
        tables = c.fetchall()
        for x in tables:
            return_tables.append(x[1])

        return return_tables