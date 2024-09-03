import mysql.connector
from mysql.connector import Error



def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='blog_db',
            user='root',
            password='123456q@',
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print("Error connecting to MySQL database", e)
        return None
    
connection = create_connection()

    