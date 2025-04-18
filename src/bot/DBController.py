import psycopg2
import re
from src.bot.config import host, user, password, db_name, port
from src import model
from src.statemachine.state import * # noqa
import logging
from datetime import datetime


class DBController:
    __initialized = False

    def __new__(cls):
        if not hasattr(cls, "instance"):
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
            port=port,
        )
        self.cursor = self.connection.cursor()

        self.max_others_tags = 20

        self.table_name = "tele_meet_users"
        # self.delete_table()
        self.tags_for_matching = """
        preferences_tags
        restrictions_tags,
        dietary,
        interests_tags,
        others_interests"""

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
            "time_last_action": "TIMESTAMP DEFAULT NULL"
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

        self.products_table_colums = {
            "id": "SERIAL PRIMARY KEY",
            "user_id": "BIGINT",
            "product": "VARCHAR(255)",
            "type": "INTEGER",
        }
        self.admin_table_columns = {
            "chat_id": "VARCHAR(255) PRIMARY KEY",
            "feedback_number": "INTEGER DEFAULT 0",
        }
        self.feedback_table_columns = {
            "id": "SERIAL PRIMARY KEY",
            "chat_id": "VARCHAR(255)",
            "text": "TEXT",
        }
        self.blocked_table_columns = {
            "chat_id": "VARCHAR(255) PRIMARY KEY",
        }
        self.create_tables()

    def delete_table(self):
        self.cursor.execute(f"DROP TABLE IF EXISTS {self.table_name}")
        self.cursor.execute("DROP TABLE IF EXISTS tele_meet_relations")
        self.cursor.execute("DROP TABLE IF EXISTS tele_meet_match")
        self.cursor.execute("DROP TABLE IF EXISTS tele_meet_products")
        self.cursor.execute("DROP TABLE IF EXISTS tele_meet_admin")
        self.cursor.execute("DROP TABLE IF EXISTS tele_meet_feedback")
        self.cursor.execute("DROP TABLE IF EXISTS tele_meet_blocked")
        self.connection.commit()

    def create_tables(self):
        self.create_query("tele_meet_users", self.users_table_columns)
        self.create_query("tele_meet_relations", self.relations_table_columns)
        self.create_query("tele_meet_match", self.match_table_columns)
        self.create_query("tele_meet_products", self.products_table_colums)
        self.create_query("tele_meet_feedback", self.feedback_table_columns)
        self.create_query("tele_meet_blocked", self.blocked_table_columns)

    def create_query(self, table_name, columns: dict):
        args = []
        for key in columns.keys():
            args.append(key + " " + columns[key])
        args = ",".join(args)
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({args})")
        self.connection.commit()

    def get_user_dict(self, id):
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
        except Exception:
            logging.exception("get_user_dict")
            return None

    def update_user_information(self, id, update_fields):
        if id is None:
            print(update_fields.keys())
            keys = ", ".join(update_fields.keys())
            values = ", ".join(
                [
                    f"{update_fields[key]}" if isinstance(update_fields[key], int) else f"'{(update_fields[key])}'"
                    for key in update_fields.keys()
                ]
            )
            print(f"INSERT INTO {self.table_name} ({keys}) VALUES ({values})")
            self.cursor.execute(f"INSERT INTO {self.table_name} ({keys}) VALUES ({values})")
        else:
            set_field = ", ".join(
                [
                    f"{field} = {value}" if isinstance(value, int) else f"{field} = '{value}'"
                    for field, value in update_fields.items()
                ]
            )
            print(f"UPDATE {self.table_name} SET {set_field} WHERE id = {id};")
            self.cursor.execute(f"UPDATE {self.table_name} SET {set_field} WHERE id = {id};")
        self.connection.commit()

    def get_user(self, id):
        user_info = self.get_user_dict(id)
        if user_info:
            user = model.User()
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

    def set_user(self, user):
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
            user.others_interests = re.split(r"[ ,]+", user.others_interests)
            for x in user.others_interests:
                if x not in tmp and x != "":
                    tmp.append(x)
            user.others_interests = " ".join(tmp[: self.max_others_tags])
            update_fields["others_interests"] = user.others_interests
        if update_fields.get("photo_file_ids", None) is not None:
            update_fields["photo_file_ids"] = ",".join(user.photo_file_ids)
        if update_fields.get("status", None) is not None:
            update_fields["status"] = user.status.value
        if update_fields.get("gender", None) is not None:
            update_fields["gender"] = user.gender.value

        update_fields["time_last_action"] = datetime.now()

        self.update_user_information(user.id, update_fields)

    def get_id_by_chat_id(self, chat_id):
        if isinstance(chat_id, str) is False:
            chat_id = str(chat_id)

        self.cursor.execute(f"SELECT id FROM {self.table_name} WHERE chat_id = '{chat_id}';")
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_user_by_chat_id(self, chat_id):
        id = self.get_id_by_chat_id(chat_id)

        if id is None:
            return model.User()
        return self.get_user(id)

    def get_user_tags(self, chat_id):
        id = self.get_id_by_chat_id(chat_id)
        if id is None:
            raise Exception("There is no current user in database")

        self.cursor.execute(f"SELECT id, {self.tags_for_matching} FROM {self.table_name} WHERE id={id}")
        return self.cursor.fetchone()

    def get_tags(self):
        self.cursor.execute(f"SELECT id, {self.tags_for_matching} FROM {self.table_name}")
        return self.cursor.fetchall()

    def get_user_relations_ids(self, id):
        self.cursor.execute(f"SELECT other_user_id FROM tele_meet_relations WHERE user_id={id}")
        return self.cursor.fetchall()

    def get_user_matches_ids(self, id):
        self.cursor.execute(f"SELECT other_user_id FROM tele_meet_match WHERE user_id={id}")
        return self.cursor.fetchall()

    def get_user_status(self, id):
        self.cursor.execute(f"SELECT status FROM {self.table_name} WHERE id={id}")
        return self.cursor.fetchone()

    def metric_number_of_users(self):
        self.cursor.execute(f"SELECT count(*) FROM {self.table_name}")
        return self.cursor.fetchone()[0]

    def metric_number_of_active_users(self, number_of_days=1):
        self.cursor.execute(f"SELECT count(*) FROM {self.table_name} \
                            WHERE time_last_action > NOW() - INTERVAL '{number_of_days} day'")
        return self.cursor.fetchone()[0]

    def metric_most_common_city(self):
        self.cursor.execute(f"SELECT city, count(*) FROM {self.table_name} \
                            WHERE city IS NOT NULL GROUP BY city \
                            ORDER BY 2 DESC \
                            LIMIT 10;")
        return self.cursor.fetchall()

    def metric_number_of_match(self):
        self.cursor.execute("SELECT count(*) FROM tele_meet_match")
        res = self.cursor.fetchone()
        if res:
            return res[0] // 2
        else:
            return 0

    def create_admin_table(self):
        self.create_query("tele_meet_admin", self.admin_table_columns)

    def add_admin(self, chat_id):
        isExist = False
        try:
            self.cursor.execute(f"INSERT INTO tele_meet_admin (chat_id) VALUES ({str(chat_id)})")
        except Exception:
            logging.info(f"user with chat_id {chat_id} already exists")
            isExist = True
        self.connection.commit()
        return isExist

    def get_all_admins(self):
        self.cursor.execute("SELECT * FROM tele_meet_admin")
        rows = self.cursor.fetchall()
        res = []
        for row in rows:
            res.append(row[0])
        return res

    def insert_feedback(self, chat_id, text):
        chat_id = str(chat_id)
        print("INSERT INTO tele_meet_feedback (chat_id, text) VALUES (%s, %s)")
        self.cursor.execute("INSERT INTO tele_meet_feedback (chat_id, text) VALUES (%s, %s)", (chat_id, text))
        self.connection.commit()

    def get_feedback_number(self, chat_id):
        self.cursor.execute("SELECT feedback_number FROM tele_meet_admin WHERE chat_id = %s", (chat_id,))
        return self.cursor.fetchone()[0]

    def get_feedback_size(self):
        self.cursor.execute("SELECT count(*) FROM tele_meet_feedback")
        res = self.cursor.fetchone()
        if not res:
            return 0
        return res[0]

    def get_feedback(self, start_id):
        self.cursor.execute("SELECT chat_id, text FROM tele_meet_feedback WHERE id > %s ORDER BY chat_id LIMIT 5",
                            (start_id,))
        rows = self.cursor.fetchall()
        res = []
        for row in rows:
            res.append((row[0], row[1]))
        return res

    def set_feedback_number(self, chat_id, new_val):
        chat_id = str(chat_id)
        print("UPDATE tele_meet_admin SET feedback_number = %s WHERE chat_id = %s;", (new_val, chat_id))
        self.cursor.execute("UPDATE tele_meet_admin SET feedback_number = %s WHERE chat_id = %s;", (new_val, chat_id))
        self.connection.commit()

    def block_user(self, chat_id):
        isExist = False
        try:
            self.cursor.execute(f"INSERT INTO tele_meet_blocked (chat_id) VALUES ({str(chat_id)})")
        except Exception:
            logging.info(f"user with chat_id {chat_id} already blocked")
            isExist = True
        self.connection.commit()
        return isExist

    def unblock_user(self, chat_id):
        isExist = False
        try:
            self.cursor.execute(f"DELETE FROM tele_meet_blocked WHERE chat_id = '{str(chat_id)}'")
        except Exception:
            logging.info(f"user with chat_id {chat_id} already unblocked")
            isExist = True
        self.connection.commit()
        return isExist

    def get_all_blocked(self):
        self.cursor.execute("SELECT * FROM tele_meet_blocked")
        rows = self.cursor.fetchall()
        res = []
        for row in rows:
            res.append(row[0])
        return res
