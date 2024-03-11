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
        self.createTables()
        # Temporary testing
        # self.cursor.execute(
        #     "SELECT version();"
        # )
        # print(self.cursor.fetchone())
        # self.cursor.execute(
        #     "CREATE TABLE IF NOT EXISTS aa (id BIGINT);"
        # )

        # self.cursor.execute(
        #     "INSERT INTO aa VALUES(10);"
        # )

        # self.cursor.execute(
        #     "SELECT * FROM aa;"
        # )
        # print(self.cursor.fetchall())
    
    def createTables(self):
        self.createQuery("tele_meet_users", 
        '''id BIGINT, 
        create_date TIMESTAMP WITHOUT TIME ZONE,
        update_date TIMESTAMP WITHOUT TIME ZONE, 
        about VARCHAR(2000), 
        active_poll_id VARCHAR(255),
        age INTEGER, 
        chat_id VARCHAR(255),
        city VARCHAR(255), 
        first_name VARCHAR(255), 
        gender VARCHAR(255),
        geolocation VARCHAR(255),
        interests_tags VARCHAR(255),
        language_code VARCHAR(255),
        last_name VARCHAR(255), 
        phone_number VARCHAR(255), 
        photo_file_ids VARCHAR(255),
        profile_name VARCHAR(255), 
        restrictions_tags VARCHAR(255), 
        state_class VARCHAR(255), 
        status VARCHAR(255), 
        username VARCHAR(255)''')

    def selectQuery(self, table_name, args):
        self.cursor.execute(f"SELECT {args} FROM {table_name}")
    
    def updateQuery(self, table_name, args):
        # not necessary
        pass
    
    def createQuery(self, table_name, args):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({args})")
    
    def insertQuery(self, table_name, args):
        self.cursor.execute(f"INSERT INTO {table_name} VALUES ({args})")