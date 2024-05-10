from abc import abstractmethod
import logging
from src.model import Update
from src import bot


class State:
    def __init__(self, context=None):
        self.next_state = self
        self.context = context

    @abstractmethod
    async def process_update(self, update: Update):
        pass

    @abstractmethod
    async def send_message(self, update: Update):
        pass

    async def go_next_state(self, update: Update):
        try:
            await self.process_update(update)
        except Exception as exc:
            logging.exception(exc)
            admins = bot.DBController().get_all_admins()
            for id in admins:
                await self.bot.send_message(id, f"An error occurred in State: {exc}")
        return self.context.state
