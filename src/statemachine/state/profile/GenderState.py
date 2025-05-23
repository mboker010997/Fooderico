from src.statemachine import State
from src.statemachine.state import profile
from aiogram import types
from src import model


class GenderState(State):
    def __init__(self, context):
        super().__init__(context)

    async def process_update(self, update: model.Update):
        if not update.get_message():
            return

        message = update.get_message()
        if self.context.user.gender is None or message.text != self.context.get_message("gender_skipBtn"):
            if message.text == self.context.get_message("gender_M"):
                gender = model.Gender.MALE
            elif message.text == self.context.get_message("gender_F"):
                gender = model.Gender.FEMALE
            else:
                return
            self.context.user.gender = gender

        self.context.set_state(profile.ProductState(self.context))
        self.context.save_to_db()

    async def send_message(self, update: model.Update):
        if not update.get_message():
            return
        message = update.get_message()

        buttons = [
            [types.KeyboardButton(text=self.context.get_message("gender_M"))],
            [types.KeyboardButton(text=self.context.get_message("gender_F"))],
        ]
        if self.context.user.gender is not None:
            buttons.append([types.KeyboardButton(text=self.context.get_message("gender_skipBtn"))])

        keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
        await message.answer(self.context.get_message("gender_text"), reply_markup=keyboard)
