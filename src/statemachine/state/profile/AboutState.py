from src.statemachine import State
from src.model import Update
from src.statemachine.state import menu
from aiogram import types


class AboutState(State):
    def __init__(self, context):
        super().__init__(context)

    def processUpdate(self, update: Update):
        if not update.getMessage():
            return
        message = update.getMessage()

        if self.context.user.about is None or message.text != self.context.getMessage("username_skipBtn"):
            self.context.user.about = message.text

        self.context.setState(menu.MenuState(self.context))
        self.context.saveToDb()

    async def sendMessage(self, update: Update):
        if not update.getMessage():
            return
        message = update.getMessage()

        if self.context.user.about:
            kb = [
                [types.KeyboardButton(text=self.context.getMessage("username_skipBtn"))],
            ]
            keyboard = types.ReplyKeyboardMarkup(
                keyboard=kb, resize_keyboard=True, one_time_keyboard=True
            )
            await message.answer(self.context.getMessage("about_text"), reply_markup=keyboard)
        else:
            await message.answer(self.context.getMessage("about_text"), reply_markup=types.ReplyKeyboardRemove())
