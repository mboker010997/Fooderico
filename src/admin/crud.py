from src.bot import DBController
import logging


table_name = "tele_meet_admin"

table_columns = {
    "chat_id": "VARCHAR(255) PRIMARY KEY",
}

controller = DBController()


def create_admin_table():
    args = []
    for key in table_columns.keys():
        args.append(key + " " + table_columns[key])
    args = ",".join(args)
    controller.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({args})')
    controller.connection.commit()


def get_all_admins():
    controller.cursor.execute(f"SELECT * FROM {table_name}")
    rows = controller.cursor.fetchall()
    res = []
    for row in rows:
        res.append(row[0])
    return res


def add_admin(chat_id):
    try:
        controller.cursor.execute(f"INSERT INTO {table_name} (chat_id) VALUES {chat_id}")
        controller.connection.commit()
    except Exception as exc:
        logging.info(f"user with chat_id {chat_id} already exists")
