from abc import abstractmethod
import logging
from src.model import Update


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
        return self.context.state
