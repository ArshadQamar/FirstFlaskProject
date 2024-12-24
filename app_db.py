import sqlite3  # Import the sqlite3 module to interact with the SQLite database
import os 

def initialize_db():
    # Establish a connection to the database (it will create the database file if it doesn't exist)
    connection = sqlite3.connect('app.db')

    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    # Execute the SQL command to create the 'users' table if it doesn't already exist
    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,          
        email TEXT UNIQUE NOT NULL,          
        password TEXT NOT NULL                 
    );
    ''')


    # Commit the changes to the database (saves the creation of the table)
    connection.commit()

    # Close the connection to the database
    connection.close()
def initialize_message_table():

    if os.path.exists('app.db'):
        # Establish a connection to the database (it will create the database file if it doesn't exist)
        connection = sqlite3.connect('app.db')

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # create message table
        cursor.execute('''
          CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_username TEXT NOT NULL,
            receiver_username TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_username) REFERENCES users(username),
            FOREIGN KEY (receiver_username) REFERENCES users(username)
            );
            ''')
        
        # Commit the changes to the database (saves the creation of the table)
        connection.commit()

        # Close the connection to the database
        connection.close()
