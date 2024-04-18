from src.statemachine import State
from src.statemachine.state import profile
from aiogram import types
from src import model


class GenderState(State):
    def __init__(self, context):
        super().__init__(context)

    async def processUpdate(self, update: model.Update):
        if not update.getMessage():
            return

        message = update.getMessage()
        if self.context.user.gender is None or message.text != self.context.getMessage("gender_skipBtn"):
            if message.text == self.context.getMessage("gender_M"):
                gender = model.Gender.MALE
            elif message.text == self.context.getMessage("gender_F"):
                gender = model.Gender.FEMALE
            else:
                return
            self.context.user.gender = gender

        self.context.setState(profile.FoodPreferencesTagState(self.context))
        self.context.saveToDb()

    async def sendMessage(self, update: model.Update):
        if not update.getMessage():
            return
        message = update.getMessage()

        buttons = [
            [types.KeyboardButton(text=self.context.getMessage("gender_M"))],
            [types.KeyboardButton(text=self.context.getMessage("gender_F"))],
        ]
        if self.context.user.gender is not None:
            buttons.append(
                [types.KeyboardButton(text=self.context.getMessage("gender_skipBtn"))]
            )

        keyboard = types.ReplyKeyboardMarkup(
            keyboard=buttons, resize_keyboard=True, one_time_keyboard=True
        )
        await message.answer(
            self.context.getMessage("gender_text"), reply_markup=keyboard
        )
