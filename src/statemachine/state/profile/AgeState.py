from src.statemachine import State
from src.statemachine.state import profile
from src.model import Update
from aiogram import types


class AgeState(State):
    def __init__(self, context):
        super().__init__(context)

    def processUpdate(self, update: Update):
        if not update.getMessage():
            return

        message = update.getMessage()
        if self.context.user.age is None or message.text != self.context.getMessage("age_skipBtn"):
            if message.text.isdigit() and (int(message.text) in range(1, 100)):
                self.context.user.age = int(message.text)
            else:
                self.text = self.context.getMessage("age_parsing_error")
                return

        self.context.setState(profile.GenderState(self.context))
        self.context.saveToDb()

    async def sendMessage(self, update: Update):
        if not update.getMessage():
            return
        message = update.getMessage()

        if self.context.user.age is not None:
            kb = [
                [types.KeyboardButton(text=self.context.getMessage("age_skipBtn"))],
            ]
            keyboard = types.ReplyKeyboardMarkup(
                keyboard=kb, resize_keyboard=True, one_time_keyboard=True
            )
            await message.answer(self.context.getMessage("age_text"), reply_markup=keyboard)
        else:
            await message.answer(self.context.getMessage("age_text"), reply_markup=types.ReplyKeyboardRemove())
