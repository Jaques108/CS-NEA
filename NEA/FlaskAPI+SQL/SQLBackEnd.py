#Import our needed modules for SQL
import sqlite3
from sqlite3 import Error

#Create a class
class SQLBackEnd:
    def __init__(self,DBFile):
        #Attributes
        self.DBFile = DBFile
        self.connection = None

    #Function for connecting to the database
    def connect(self):
        try:
            self.connection = sqlite3.connect(self.DBFile)
            print('connect to database')
        #If fails we return error with the error code which is stored in the variable e
        except Error as e:
            print(f'error connecting to database {e}')

    #Function to create our database table
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
                    print(params)
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
            print(f'Error - {e}')
            return e


    def closeConnection(self):
        if self.connection:
            self.connection.close()


#A thing that runs to reset the user IDs
conn = sqlite3.connect('main.db')
cursor = conn.cursor()

# Retrieve all user data from the users table
cursor.execute("SELECT id, password, username FROM users ORDER BY id")
users = cursor.fetchall()

# Reassign ids starting from 1
for new_id, user in enumerate(users, start=1):
    cursor.execute(
        "UPDATE users SET id = ? WHERE id = ?",
        (new_id, user[0])  # Update the ID field to be sequential
    )

# Commit the changes
conn.commit()

# Close the connection
conn.close()



if __name__ == '__main__':
    SQL = SQLBackEnd('main.db')
    SQL.connect()

    createTableScript = '''CREATE TABLE IF NOT EXISTS users
    (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL);'''

    SQL.createTable(createTableScript)



    insertUser = 'INSERT INTO users (username,password) VALUES (?,?)'