from src.statemachine import State
from src.model import Update
from src.statemachine.state import menu
from src import bot
from aiogram import types


class FeedbackState(State):
    def __init__(self, context):
        super().__init__(context)

    async def process_update(self, update: Update):
        if not update.get_message():
            return
        message = update.get_message()

        if message.text and message.text != self.context.get_message("feedback_back"):
            bot.DBController().insert_feedback(self.context.user.chat_id, message.text)

        self.context.set_state(menu.MenuState(self.context))
        self.context.save_to_db()

    async def send_message(self, update: Update):
        if not update.get_message():
            return
        message = update.get_message()

        buttons = [
            [types.KeyboardButton(text=self.context.get_message("feedback_back"))],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
        await message.answer(self.context.get_message("feedback_text"), reply_markup=keyboard)
