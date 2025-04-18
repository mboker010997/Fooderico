from src.statemachine import State
from src.statemachine.state.profile import UsernameState
from aiogram import types
from src import model


class RegisterState(State):
    def __init__(self, context):
        super().__init__(context)
        self.is_error = False

    async def process_update(self, update: model.Update):
        if not update.get_message():
            return
        message = update.get_message()
        if message.contact is None:
            self.is_error = True
            return
        user = self.context.user
        user.first_name = message.contact.first_name
        user.last_name = message.contact.last_name
        user.phone_number = message.contact.phone_number
        self.context.user = user
        self.context.set_state(UsernameState(self.context))
        self.context.save_to_db()

    async def send_message(self, update: model.Update):
        if not update.get_message():
            return
        message = update.get_message()
        buttons = [
            [types.KeyboardButton(text=self.context.get_message("register_regBtn"), request_contact=True)],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
        await message.answer(
            self.context.get_message("register_error" if self.is_error else "register_text"),
            reply_markup=keyboard,
        )
