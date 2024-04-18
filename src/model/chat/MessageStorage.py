import asyncio


class MessageStorage:
    def __init__(self):
        self.messages = dict()
        self.closed = set()
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

    async def close(self, from_user, to_user):
        key = (from_user, to_user)
        async with self.lock:
            self.closed.add(key)

    async def open(self, from_user, to_user):
        key = (from_user, to_user)
        async with self.lock:
            if key in self.closed:
                self.closed.remove(key)

    async def is_closed(self, from_user, to_user):
        key = (from_user, to_user)
        async with self.lock:
            result = (key in self.closed)
        return result
