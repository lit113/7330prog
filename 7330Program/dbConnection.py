"""import mysql.connector
from mysql.connector import connect, Error

def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='cs5330',
            password='pw5330',
            database='dbprog'
        )
        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_info)
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None"""
