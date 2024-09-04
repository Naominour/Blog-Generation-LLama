import mysql.connector
from mysql.connector import Error



def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Your MySQL host (use 'localhost' or an IP address)
            database='blog_db',  # Your database name
            user='root',  # Your MySQL username
            password='hessam'  # Your MySQL password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        st.error(f"Error connecting to MySQL database: {e}")
        return None

# Initialize MySQL connection
connection = create_connection()
    