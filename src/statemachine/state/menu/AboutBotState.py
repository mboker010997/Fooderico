from src.statemachine import State
from src.model import Update
from src.statemachine.state import menu
from aiogram.enums import ParseMode


class AboutBotState(State):
    def __init__(self, context):
        super().__init__(context)

    def processUpdate(self, update: Update):
        pass

    async def sendMessage(self, update: Update):
        if not update.getMessage():
            return
        message = update.getMessage()
        await message.answer(self.context.getMessage("aboutBot_text"),
                             parse_mode=ParseMode.HTML)
        await message.answer(self.context.getMessage("returned_into_menu"))
        self.context.setState(menu.MenuState(self.context))
        self.context.saveToDb()
