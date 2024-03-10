from abc import abstractmethod
import logging


class State:
    def __init__(self):
        self.nextState = self
    
    @abstractmethod
    def processUpdate(self, message):
        pass

    @abstractmethod
    def getNextState(self, message):
        pass

    @abstractmethod
    async def sendMessage(self, message, bot, dp):
        pass

    def goNextState(self, message):
        try:
            self.processUpdate(message)
        except Exception as exc:
            logging.error(exc)
        return self.getNextState(message)
    