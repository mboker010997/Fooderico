from abc import abstractmethod
import logging
from src.model import Update


class State:
    def __init__(self, context=None):
        self.nextState = self
        self.context = context

    @abstractmethod
    async def processUpdate(self, update: Update):
        pass

    @abstractmethod
    async def sendMessage(self, update: Update):
        pass

    async def goNextState(self, update: Update):
        try:
            await self.processUpdate(update)
        except Exception as exc:
            logging.exception(exc)
        return self.context.state
