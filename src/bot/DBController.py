import psycopg2
from config import *

class DBController:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            port=port
        )
        self.cursor = self.connection.cursor()

        # Temporary testing
        self.cursor.execute(
            "SELECT version();"
        )
        print(self.cursor.fetchone())
    
    def createTables(self):
        pass

    def selectQuery(self, table_name, args):
        pass
    
    def updateQuery(self, table_name, args):
        pass
    
    def createQuery(self, table_name, args):
        pass