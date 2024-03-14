from src.statemachine.State import State
from src.bot.Update import Update


class AboutState(State):
    def __init__(self):
        super().__init__()

    def processUpdate(self, update: Update):
        pass

    def getNextState(self, update: Update):
        pass

    async def sendMessage(self, update: Update):
        message = update.getMessage()
        await message.answer("Напишите информацию о себе")
