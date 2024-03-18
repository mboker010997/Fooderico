import psycopg2
from config import *
from src.model.User import User
## import all classes

class DBController:
    __initialized = False

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DBController, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        if self.__initialized:
            return
        self.__initialized = True
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            port=port
        )
        self.cursor = self.connection.cursor()
        self.createTables()
        
        self.table_name = 'tele_meet_users'
        
        # Temporary testing
        # self.cursor.execute(
        #     "SELECT version();"
        # )
        # print(self.cursor.fetchone())
        # self.cursor.execute(
        #     "CREATE TABLE IF NOT EXISTS aa (id BIGINT);"
        # )

        # self.cursor.execute(
        #     "INSERT INTO aa VALUES(13);"
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
    
    def getUserDict(self, id):
        try:
            self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = %s;", (id,))
            row = self.cursor.fetchone()
            if row:
                columns_info = {
                    "id": row[0],
                    "create_date": row[1],
                    "update_date": row[2],
                    "about": row[3],
                    "active_poll_id": row[4],
                    "age": row[5],
                    "chat_id": row[6],
                    "city": row[7],
                    "first_name": row[8],
                    "gender": row[9],
                    "geolocation": row[10],
                    "language_code": row[11],
                    "last_name": row[12],
                    "phone_number": row[13],
                    "photo_file_ids": row[14],
                    "profile_name": row[15],
                    "restrictions_tags": row[16],
                    "state_class": row[17],
                    "status": row[18],
                    "username": row[19]
                }
                return columns_info
            else:
                return None
        except Exception as exc:
            print(f'Exception: {exc}')
            return None 
    
    def updateUserInformation(self, id, update_fields):
        set_field = ", ".join([f"{field} = {value}" if isinstance(value, int)
                                else f"{field} = '{value}'"
                                for field, value in update_fields.items()])
        try:
            self.cursor.execute(f"UPDATE {self.table_name} SET {set_field} WHERE id = {id};")
            self.connection.commit()
        except Exception as exc:
            print(f'Exception: {exc}')
    
    def updateState(self, id, state):
        return self.updateUserInformation(id, {"state_class": state})
     
    def getClass(self, class_name):
        return globals()[class_name]

    def getState(self, id):
        self.cursor.execute(f"SELECT state_class FROM {self.table_name} WHERE id = {id};")
        result = self.cursor.fetchone()
        state_class_name = result[0] if result else None
        if state_class_name:
            return self.getClass(state_class_name)
        else:
            return None
        
    def getUser(self, id):
        user_info = self.getUserDict(id)
        if user_info:
            user = User()
            user.id = user_info["id"]
            user.age = user_info["age"]
            user.create_date = user_info["create_date"]
            user.update_date = user_info["update_date"]
            user.city = user_info["city"]
            user.first_name = user_info["first_name"]
            user.gender = user_info["gender"]
            user.geolocation = user_info["geolocation"]
            user.language_code = user_info["language_code"]
            user.last_name = user_info["last_name"]
            user.phone_number = user_info["phone_number"]
            user.photo_file_ids = user_info["photo_file_ids"]
            user.profile_name = user_info["profile_name"]
            user.restrictions_tags = user_info["restrictions_tags"]
            user.state_class = user_info["state_class"]
            user.status = user_info["status"]
            user.username = user_info["username"]
            user.about = user_info["about"]
            user.active_poll_id = user_info["active_poll_id"]
            user.chat_id = user_info["chat_id"]
            return user
        else:
            return None
        
    def setUser(self, user):
        update_fields = {}
        for column_name, value in vars(user).items():
            if value is not None:
                update_fields[column_name] = value
        
        self.updateUserInformation(user.id, update_fields)
        
    def getUserByChatId(self, chat_id):
        if isinstance(chat_id, str) is False:
            chat_id = str(chat_id)
        
        self.cursor.execute(f"SELECT id FROM {self.table_name} WHERE chat_id = '{chat_id}';")
        result = self.cursor.fetchone()
        id = result[0] if result else None
        if id is None:
            return User()
        return self.getUser(id)
