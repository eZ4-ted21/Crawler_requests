import psycopg2
import os
from psycopg2 import OperationalError

class GetDBConnection():
    '''
    A class that represents database connection

    methods :
        getConnection() : establish database connection
    '''

    def __init__(self):
        """
        Initialize a new instance of a class
        """
        pass

    def getConnection(self):
        """
        connection (tupple) : established connection parameters such as port, host, dbname, user and password
        cursor : established connection cursor
        
        Behaviour : 
            - established database connection
            - checks if datbase connection status
            - Returns databse connection
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

        except OperationalError as e:
            print("Error:", e)
        return connection