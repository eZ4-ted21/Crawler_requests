import psycopg2
import os
from psycopg2 import OperationalError

class GetDBConnection:
    """
    A class that represents database connection

    methods :
        getConnection() : establish database connection
    """

    def __init__(self):
        """
        Initialize a new instance of a class
        """
        pass

    @staticmethod
    def get_connection():
        """
        connection (tuple) : established connection parameters such as port, host, dbname, user and password
        cursor : established connection cursor
        
        Behavior :
            - established database connection
            - checks if database connection status
            - Returns database connection
        """
        try:
            connection = psycopg2.connect(
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('DB_USERNAME'),
                password=os.getenv('DB_PASS'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT')
            )
            print("Connection established successfully!")
            return connection
        except OperationalError as e:
            print("Error:", e)