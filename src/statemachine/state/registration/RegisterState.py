from src.statemachine import State
from src.statemachine.state.profile import UsernameState
from aiogram import types
from src import model


class RegisterState(State):
    def __init__(self, context):
        super().__init__(context)

    async def sendMessage(self, update: model.Update):
        message = update.getMessage()
        kb = [
            [types.KeyboardButton(text="Регистрация", request_contact=True)],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
        await message.answer("Добро пожаловать в TeleMeetBot для регистрации предоставьте контакт",
                             reply_markup=keyboard)

    def processUpdate(self, update: model.Update):
        message = update.getMessage()
        user = self.context.user
        user.first_name = message.contact.first_name
        user.last_name = message.contact.last_name
        user.phone_number = message.contact.phone_number
        user.status = model.Status.ENABLED
        self.context.user = user

        self.context.setState(UsernameState(self.context))
        self.context.saveToDb()
