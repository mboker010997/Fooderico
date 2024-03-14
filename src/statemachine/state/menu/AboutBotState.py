from src.statemachine.State import State
from src.bot.Update import Update
from src.statemachine.state.menu.MenuState import MenuState


class AboutBotState(State):
    def __init__(self):
        super().__init__()

    def processUpdate(self, update: Update):
        pass

    def getNextState(self, update: Update):
        return MenuState()

    async def sendMessage(self, update: Update):
        message = update.getMessage()
        await message.answer("О боте...")


