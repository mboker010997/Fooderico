from src.statemachine import State
from src.statemachine.state import profile
from aiogram import types
from src.model import Update


class UsernameState(State):
    def __init__(self, context):
        super().__init__(context)

    async def sendMessage(self, update: Update):
        message = update.getMessage()
        kb = [
            [types.KeyboardButton(text="Оставь текущее")],
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb, resize_keyboard=True, one_time_keyboard=True
        )
        await message.answer("Введите имя", reply_markup=keyboard)

    def processUpdate(self, update: Update):
        message = update.getMessage()
        if message.text != "Оставь текущее":
            self.context.user.profile_name = message.text
        self.context.setState(profile.AgeState(self.context))
        self.context.saveToDb()
