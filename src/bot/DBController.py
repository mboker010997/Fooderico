import psycopg2
import re
from config import *
from src.model.User import User
from src.statemachine.state import *


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

        self.table_name = 'tele_meet_users'
        self.deleteTable()
        self.tags_for_matching = '''
        preferences_tags
        restrictions_tags,
        interests_tags'''

        self.users_table_columns = {
            "id": "SERIAL PRIMARY KEY",
            "create_date": "TIMESTAMP WITHOUT TIME ZONE",
            "update_date": "TIMESTAMP WITHOUT TIME ZONE",
            "about": "VARCHAR(2000)",
            "active_poll_id": "VARCHAR(255)",
            "age": "INTEGER",
            "chat_id": "VARCHAR(255)",
            "city": "VARCHAR(255)",
            "first_name": "VARCHAR(255)",
            "gender": "VARCHAR(255)",
            "geolocation": "VARCHAR(255)",
            "language_code": "VARCHAR(255)",
            "last_name": "VARCHAR(255)",
            "phone_number": "VARCHAR(255)",
            "photo_file_ids": "VARCHAR(255)",
            "profile_name": "VARCHAR(255)",
            "state_class": "VARCHAR(255)",
            "status": "VARCHAR(255)",
            "username": "VARCHAR(255)",
            "food_preferance_and_goals": "VARCHAR(255)",
            "restrictions_tags": "VARCHAR(255)",
            "dietary": "VARCHAR(255)",
            "interests_tags": "VARCHAR(255)",
            "others_interests": "VARCHAR(255)",
        }

        self.relations_table_columns = {
            "id": "SERIAL PRIMARY KEY",
            "user_id": "BIGINT",
            "other_user_id": "BIGINT",
            "relation": "VARCHAR(20) NOT NULL",
        }

        self.createTables()

    def deleteTable(self):
        self.cursor.execute(f"DROP TABLE IF EXISTS {self.table_name}")
        self.connection.commit()
    
    def createTables(self):
        self.createQuery("tele_meet_users", self.users_table_columns)
        self.createQuery("tele_meet_relations", self.relations_table_columns)

    def selectQuery(self, table_name, args):
        self.cursor.execute(f"SELECT {args} FROM {table_name}")

    def createQuery(self, table_name, columns: dict):
        args = []
        for key in columns.keys():
            args.append(key + " " + columns[key])
        args = ",".join(args)
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({args})")
        self.connection.commit()
    
    def insertQuery(self, table_name, args: dict):
        columns = ",".join(args.keys())
        values = ",".join(map(lambda x: str(x) if isinstance(x, int) else f"'{x}'", args.values()))
        self.cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({values})")
        self.connection.commit()
    
    def getUserDict(self, id):
        try:
            self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = %s;", (id,))
            row = self.cursor.fetchone()
            if row:
                columns_info = dict()
                curIndex = 0
                for key in self.users_table_columns:
                    columns_info[key] = row[curIndex]
                    curIndex += 1
                return columns_info
            else:
                return None
        except Exception as exc:
            print(f'Exception: {exc}')
            return None
    
    def updateUserInformation(self, id, update_fields):
        if id is None:
            print(update_fields.keys())
            keys = ", ".join(update_fields.keys())
            values = ", ".join([f"{update_fields[key]}" if isinstance(update_fields[key], int)
                                    else f"'{(update_fields[key])}'"
                                    for key in update_fields.keys()])
            print(f"INSERT INTO {self.table_name} ({keys}) VALUES ({values})")
            self.cursor.execute(f"INSERT INTO {self.table_name} ({keys}) VALUES ({values})")
        else:
            set_field = ", ".join([f"{field} = {value}" if isinstance(value, int)
                            else f"{field} = '{value}'"
                            for field, value in update_fields.items()])
            print(f"UPDATE {self.table_name} SET {set_field} WHERE id = {id};")
            self.cursor.execute(f"UPDATE {self.table_name} SET {set_field} WHERE id = {id};")
        self.connection.commit()
    
    def updateState(self, chat_id, state):
        return self.updateUserInformation(self.getIdByChatId(chat_id),
                                          {"state_class": state.__class__.__name__})
        
    def getUser(self, id):
        user_info = self.getUserDict(id)
        if user_info:
            user = User()
            for key in user_info:
                setattr(user, key, user_info[key])
            if user.state_class is not None:
                user.state_class = globals()[user.state_class]
            if user.restrictions_tags is not None:
                user.restrictions_tags = set(user.restrictions_tags.split(","))
            if user.interests_tags is not None:
                user.interests_tags = set(user.interests_tags.split(","))
            if user.photo_file_ids is not None:
                if user.photo_file_ids != "":
                    user.photo_file_ids = user.photo_file_ids.split(",")
                else:
                    user.photo_file_ids = list()
            return user
        else:
            return None
        
    def setUser(self, user):
        update_fields = {}
        for column_name, value in vars(user).items():
            if value is not None and column_name != "id":
                update_fields[column_name] = value
        if update_fields.get("state_class", None) is not None:
            update_fields["state_class"] = user.state_class.__name__
        if update_fields.get("restrictions_tags", None) is not None:
            update_fields["restrictions_tags"] = ",".join(list(user.restrictions_tags))
        if update_fields.get("interests_tags", None) is not None:
            update_fields["interests_tags"] = ",".join(list(user.interests_tags))
        if update_fields.get("photo_file_ids", None) is not None:
            update_fields["photo_file_ids"] = ",".join(user.photo_file_ids)
        
        self.updateUserInformation(user.id, update_fields)
    
    def getIdByChatId(self, chat_id):
        if isinstance(chat_id, str) is False:
            chat_id = str(chat_id)
        
        self.cursor.execute(f"SELECT id FROM {self.table_name} WHERE chat_id = '{chat_id}';")
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def getChatIdById(self, id):
        if isinstance(id, int) is False:
            id = int(id)
        
        self.cursor.execute(f"SELECT chat_id FROM {self.table_name} WHERE id = '{id}';")
        result = self.cursor.fetchone()
        return result[0] if result else None
        
    def getUserByChatId(self, chat_id):
        id = self.getIdByChatId(chat_id)

        if id is None:
            return User()
        return self.getUser(id)

    def matchOneTag(self, first_answers, second_answers):
        list_first_answers = re.split(', |,', first_answers)
        list_second_answers = re.split(', |,', second_answers)

        list_first_answers.sort()
        list_second_answers.sort()

        count_matches = 0
        for answer_first in list_first_answers:
            for answer_second in list_second_answers:
                if answer_first == answer_second:
                    count_matches += 1
        return count_matches


    def tagsMatchingQueue(self, chat_id):
        id = self.getIdByChatId(chat_id)

        self.cursor.execute(f"SELECT id, {self.tags_for_matching} FROM {self.table_name} WHERE id={id}")
        current_tags = self.cursor.fetchone()

        self.cursor.execute(f"SELECT id, {self.tags_for_matching} FROM {self.table_name}")
        list_of_tags = self.cursor.fetchall()

        matching_queue = []
        for person_tags in list_of_tags:
            count_matches = 0
            for tag_position in range(1, len(person_tags)):
                count_matches += self.matchOneTag(person_tags[tag_position], current_tags[tag_position])
            matching_queue.append((count_matches, person_tags[0]))
        matching_queue.sort(reverse=True)
        
        return [id for count_matches, id in matching_queue[1:]]
