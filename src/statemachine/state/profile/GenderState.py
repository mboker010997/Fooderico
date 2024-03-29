from src.statemachine import State
from src.statemachine.state import profile
from aiogram import types
from src import model


class GenderState(State):
    def __init__(self, context):
        super().__init__(context)

    def processUpdate(self, update: model.Update):
        if not update.getMessage():
            return
        message = update.getMessage()
        if message.text == self.context.getMessage("gender_M"):
            gender = model.Gender.MALE
        elif message.text == self.context.getMessage("gender_F"):
            gender = model.Gender.FEMALE
        else:
            return
        self.context.user.gender = gender
        self.context.setState(profile.RestrictionsTagState(self.context))
        self.context.saveToDb()

    async def sendMessage(self, update: model.Update):
        if not update.getMessage():
            return
        message = update.getMessage()
        kb = [
            [types.KeyboardButton(text=self.context.getMessage("gender_M"))],
            [types.KeyboardButton(text=self.context.getMessage("gender_F"))],
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb, resize_keyboard=True, one_time_keyboard=True
        )
        await message.answer(self.context.getMessage("gender_text"), reply_markup=keyboard)
