from src.statemachine import State
from src.model import Update
from src.statemachine.state import menu


class AboutBotState(State):
    def __init__(self, context):
        super().__init__(context)

    def processUpdate(self, update: Update):
        pass

    async def sendMessage(self, update: Update):
        message = update.getMessage()
        await message.answer("О боте...")
        self.context.setState(menu.MenuState(self.context))
        self.context.saveToDb()
