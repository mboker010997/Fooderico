from src.statemachine.State import State
from src.statemachine.state.profile.UsernameState import UsernameState
from aiogram import types


class RegisterState(State):
    def __init__(self):
        super().__init__()

    def processUpdate(self, message):
        pass

    def getNextState(self, message):
        return UsernameState()

    async def sendMessage(self, message, bot, dp):
        kb = [
            [types.KeyboardButton(text="Регистрация", request_contact=True)],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, one_time_keyboard=True)
        await message.answer("Добро пожаловать в TeleMeetBot для регистрации предоставьте контакт",
                             reply_markup=keyboard)
