import asyncio
from src.bot import DBController

table_name = "tele_meet_messages"
table_columns = {
    "id": "SERIAL PRIMARY KEY",
    "from_user_id": "VARCHAR(255)",
    "to_user_id": "VARCHAR(255)",
    "message_text": "VARCHAR(2000)",
}


def create_message_table():
    controller = DBController()
    args = []
    for key in table_columns.keys():
        args.append(key + " " + table_columns[key])
    args = ",".join(args)
    controller.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({args})')
    controller.connection.commit()


class MessageStorage:
    def __init__(self):
        self.messages = dict()
        self.opened = set()
        self.lock = asyncio.Lock()

    async def dump_messages(self, from_user, to_user):
        key = (from_user, to_user)
        async with self.lock:
            result_list = self.messages.get(key, [])
            if key in self.messages:
                self.messages.pop(key)
        return result_list

    async def put_message(self, from_user, to_user, message):
        key = (from_user, to_user)
        async with self.lock:
            if key not in self.messages:
                self.messages[key] = []
            self.messages[key].append(message)

        # controller = DBController()
        # controller.cursor.execute(f"INSERT INTO {table_name} (from_user_id, to_user_id, message_text) "
        #                           f"VALUES ({from_user}, {to_user}, '{message}')")
        # controller.connection.commit()

    async def close(self, from_user, to_user):
        key = (from_user, to_user)
        async with self.lock:
            if key in self.opened:
                self.opened.remove(key)

    async def open(self, from_user, to_user):
        key = (from_user, to_user)
        async with self.lock:
            self.opened.add(key)

    async def is_closed(self, from_user, to_user):
        key = (from_user, to_user)
        async with self.lock:
            result = key not in self.opened
        return result
