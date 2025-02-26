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
            #If there is a connection then do this
            if self.connection:
                cursor = self.connection.cursor()
                cursor.execute(createTableScript)

            #If not we return Error
            else:
                print('error')

        except Error as e:
            print(f'error connecting to database {e}')

    # Function to execute a SQL Query
    def executeQuery(self, queryScript, params=None):
        try:
            # Check if there is an active database connection
            if self.connection:
                cursor = self.connection.cursor()  # Create a cursor object for executing SQL commands

                # If parameters are provided, execute the query with parameters
                if params:
                    print(params)  # Print the parameters for debugging
                    cursor.execute(queryScript, params)
                else:
                    # Execute the query without parameters
                    cursor.execute(queryScript)

                self.connection.commit()  # Commit the transaction
                print('Query executed successfully')

                return cursor.fetchall()  # Return all fetched results

            else:
                print('no connection')  # If no connection is found, print an error message
                return None

        except Error as e:
            # Handle any exceptions that occur during execution
            print(f'Error - {e}')
            return e  # Return the error for further handling

    # Function to close the database connection
    def closeConnection(self):
        if self.connection:
            # Close the database connection
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


#Run the program
if __name__ == '__main__':
    #Connect to the database
    SQL = SQLBackEnd('main.db')
    SQL.connect()

    #An SQL script to create the table if it doesn't exist
    createTableScript = '''CREATE TABLE IF NOT EXISTS users
    (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL);'''

    #Create the table using the script
    SQL.createTable(createTableScript)


    #Another script for adding a user to the table
    insertUser = 'INSERT INTO users (username,password) VALUES (?,?)'