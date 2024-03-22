from src.statemachine import State
from src.model import Update
from src.statemachine.state import menu


class AboutState(State):
    def __init__(self, context):
        super().__init__(context)

    def processUpdate(self, update: Update):
        self.context.user.about = update.getMessage().text
        self.context.setState(menu.MenuState(self.context))
        self.context.saveToDb()

    async def sendMessage(self, update: Update):
        message = update.getMessage()
        await message.answer(self.context.getMessage("about_text"))
