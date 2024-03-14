from abc import abstractmethod
import logging
from src.bot.Update import Update
from aiogram import Bot, Dispatcher


class State:
    def __init__(self):
        self.nextState = self
    
    @abstractmethod
    def processUpdate(self, update: Update):
        pass

    @abstractmethod
    def getNextState(self, update: Update):
        pass

    @abstractmethod
    async def sendMessage(self, update: Update):
        pass

    def goNextState(self, update: Update):
        try:
            self.processUpdate(update)
        except Exception as exc:
            logging.error(exc)
        return self.getNextState(update)
    