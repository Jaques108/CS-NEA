import sqlite3
from sqlite3 import Error

class SQLBackEnd:
    def __init__(self,DBFile):
        self.DBFile = DBFile
        self.connection = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.DBFile)
            print('connect to database')

        except Error as e:
            print(f'error connecting to database {e}')

    def createTable(self,createTableScript):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                cursor.execute(createTableScript)

            else:
                print('error')

        except Error as e:
            print(f'error connecting to database {e}')


    def executeQuery(self,queryScript,params = None):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                if params:
                    cursor.execute(queryScript,params)
                else:
                    cursor.execute(queryScript)

                self.connection.commit()
                print('Query executed successfully')

                return cursor.fetchall()

            else:
                print('no connection')
                return None

        except Error as e:
            print(f'Error {e}')
            return e


    def closeConnection(self):
        if self.connection:
            self.connection.close()




if __name__ == '__main__':
    SQL = SQLBackEnd('main.db')
    SQL.connect()

    createTableScript = '''CREATE TABLE IF NOT EXISTS users
    (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL);'''

    SQL.createTable(createTableScript)

    insertUser = 'INSERT INTO users (username,password) VALUES (?,?)'





