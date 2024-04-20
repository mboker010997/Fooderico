from src.statemachine import State
from src.statemachine.state import profile
from src.model import Update
from aiogram import types


class AgeState(State):
    def __init__(self, context):
        super().__init__(context)
        self.text = self.context.get_message("age_text")

    async def process_update(self, update: Update):
        if not update.get_message():
            return

        message = update.get_message()
        if self.context.user.age is None or message.text != self.context.get_message("age_skipBtn"):
            if message.text.isdigit() and (int(message.text) in range(1, 100)):
                self.context.user.age = int(message.text)
            else:
                self.text = self.context.get_message("age_parsing_error")
                return

        self.context.set_state(profile.GenderState(self.context))
        self.context.save_to_db()

    async def send_message(self, update: Update):
        if not update.get_message():
            return
        message = update.get_message()

        if self.context.user.age is not None:
            buttons = [
                [types.KeyboardButton(text=self.context.get_message("age_skipBtn"))],
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
            await message.answer(self.text, reply_markup=keyboard)
        else:
            await message.answer(self.text, reply_markup=types.ReplyKeyboardRemove())
