from src.statemachine.State import State
from src.bot.Update import Update
import src.statemachine.state.menu as menu


class AboutState(State):
    def __init__(self):
        super().__init__()

    def processUpdate(self, update: Update):
        pass

    def getNextState(self, update: Update):
        return menu.MenuState()

    async def sendMessage(self, update: Update):
        message = update.getMessage()
        await message.answer("Напишите информацию о себе")
