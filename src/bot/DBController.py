import psycopg2
import re
from config import *
from src.model.User import User
from src.statemachine.state import *
from src import model
import logging


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

        self.max_others_tags = 20

        self.table_name = 'tele_meet_users'
        # self.deleteTable()
        self.tags_for_matching = '''
        preferences_tags
        restrictions_tags,
        dietary,
        interests_tags,
        others_interests'''

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
            "photo_file_ids": "VARCHAR(1000)",
            "profile_name": "VARCHAR(255)",
            "state_class": "VARCHAR(255)",
            "status": "VARCHAR(255)",
            "username": "VARCHAR(255)",
            "food_preferance_and_goals": "VARCHAR(255)",
            "restrictions_tags": "VARCHAR(1000)",
            "dietary": "VARCHAR(1000)",
            "interests_tags": "VARCHAR(1000)",
            "others_interests": "VARCHAR(1000)",
            "preferences_tags": "VARCHAR(1000)",
        }

        self.relations_table_columns = {
            "id": "SERIAL PRIMARY KEY",
            "user_id": "BIGINT",
            "other_user_id": "BIGINT",
            "relation": "VARCHAR(20) NOT NULL",
        }

        self.match_table_columns = {
            "id": "SERIAL PRIMARY KEY",
            "user_id": "BIGINT",
            "other_user_id": "BIGINT",
        }

        self.createTables()

    def deleteTable(self):
        self.cursor.execute(f"DROP TABLE IF EXISTS {self.table_name}")
        self.cursor.execute("DROP TABLE IF EXISTS tele_meet_relations")
        self.cursor.execute("DROP TABLE IF EXISTS tele_meet_match")
        self.connection.commit()
    
    def deleteUser(self, chat_id):
        id = self.getIdByChatId(chat_id)

        print(id)
        self.cursor.execute(f"DELETE FROM {self.table_name} WHERE id={id}")
        # print(self.cursor.fetchall())


        self.cursor.execute(f"DELETE FROM tele_meet_relations WHERE user_id={id} or other_user_id={id}")
        # print(self.cursor.fetchall())

        self.connection.commit()
    
    def createTables(self):
        self.createQuery("tele_meet_users", self.users_table_columns)
        self.createQuery("tele_meet_relations", self.relations_table_columns)
        self.createQuery("tele_meet_match", self.match_table_columns)

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
            logging.exception("getUserDict")
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
            if user.preferences_tags is not None:
                user.preferences_tags = set(user.preferences_tags.split(","))
            if user.restrictions_tags is not None:
                user.restrictions_tags = set(user.restrictions_tags.split(","))
            if user.dietary is not None:
                user.dietary = set(user.dietary.split(","))
            if user.interests_tags is not None:
                user.interests_tags = set(user.interests_tags.split(","))
            if user.others_interests is not None:
                user.others_interests = " ".join(user.others_interests.split(" "))
            if user.photo_file_ids is not None:
                if user.photo_file_ids != "":
                    user.photo_file_ids = user.photo_file_ids.split(",")
                else:
                    user.photo_file_ids = list()
            if user.status is not None:
                user.status = model.Status(user.status)
            if user.gender is not None:
                user.gender = model.Gender(user.gender)
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
        if update_fields.get("preferences_tags", None) is not None:
            update_fields["preferences_tags"] = ",".join(list(user.preferences_tags))
        if update_fields.get("restrictions_tags", None) is not None:
            update_fields["restrictions_tags"] = ",".join(list(user.restrictions_tags))
        if update_fields.get("dietary", None) is not None:
            update_fields["dietary"] = ",".join(list(user.dietary))
        if update_fields.get("interests_tags", None) is not None:
            update_fields["interests_tags"] = ",".join(list(user.interests_tags))
        if update_fields.get("others_interests", None) is not None:
            tmp = []
            user.others_interests = re.split(r'[ ,]+', user.others_interests)
            for x in user.others_interests:
                if x not in tmp and x != '':
                    tmp.append(x)
            user.others_interests = " ".join(tmp[:self.max_others_tags])
            update_fields["others_interests"] = user.others_interests
        if update_fields.get("photo_file_ids", None) is not None:
            update_fields["photo_file_ids"] = ",".join(user.photo_file_ids)
        if update_fields.get("status", None) is not None:
            update_fields["status"] = user.status.value
        if update_fields.get("gender", None) is not None:
            update_fields["gender"] = user.gender.value
        
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
    
    def getUserTags(self, chat_id):
        id = self.getIdByChatId(chat_id)
        if id is None:
            raise Exception("There is no current user in database")
        
        self.cursor.execute(f"SELECT id, {self.tags_for_matching} FROM {self.table_name} WHERE id={id}")
        return self.cursor.fetchone()

    def getTags(self):
        self.cursor.execute(f"SELECT id, {self.tags_for_matching} FROM {self.table_name}")
        return self.cursor.fetchall()
    
    def getUserRelationsIds(self, id):
        self.cursor.execute(f"SELECT other_user_id FROM tele_meet_relations WHERE user_id={id}")
        return self.cursor.fetchall()

    def getUserStatus(self, id):
        self.cursor.execute(f"SELECT status FROM {self.table_name} WHERE id={id}")
        return self.cursor.fetchone()

    def getUserMatchesIds(self, id):
        self.cursor.execute(f"SELECT other_user_id FROM tele_meet_match WHERE user_id={id}")
        return self.cursor.fetchall()


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
