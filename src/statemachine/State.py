from abc import abstractmethod
import logging 

class State:
    def __init__(self, bot, dp):
        self.bot = bot
        self.dp = dp
    
    @abstractmethod
    def processUpdate(self, message):
        pass

    @abstractmethod
    def getNextState(self, message):
        pass

    @abstractmethod
    async def sendMessage(self, message):
        pass

    def goNextState(self, message):
        try:
            self.processUpdate(message)
        except Exception as exc:
            logging.error(exc)
        return self.getNextState(message)

    