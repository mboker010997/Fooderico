from src.statemachine import State
from src.statemachine.state import profile
from aiogram import types
from src.model import Update


class UsernameState(State):
    def __init__(self, context):
        super().__init__(context)

    async def process_update(self, update: Update):
        if not update.getMessage():
            return

        message = update.getMessage()
        if self.context.user.profile_name is None or message.text != self.context.get_message("username_skipBtn"):
            self.context.user.profile_name = message.text
        self.context.set_state(profile.PhotoSelectionState(self.context))
        self.context.save_to_db()

    async def send_message(self, update: Update):
        if not update.getMessage():
            return
        message = update.getMessage()

        if self.context.user.profile_name is not None:
            buttons = [
                [types.KeyboardButton(text=self.context.get_message("username_skipBtn"))],
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
            await message.answer(self.context.get_message("username_text"), reply_markup=keyboard)
        else:
            await message.answer(
                self.context.get_message("username_text"),
                reply_markup=types.ReplyKeyboardRemove(),
            )
