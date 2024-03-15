from src.statemachine.State import State
from src.statemachine.state.profile.UsernameState import UsernameState
from aiogram import types
from src.bot.Update import Update
from aiogram import Bot, Dispatcher


class RegisterState(State):
    def __init__(self):
        super().__init__()

    def processUpdate(self, update: Update):
        pass

    def getNextState(self, update: Update):
        return UsernameState()

    async def sendMessage(self, update: Update):
        message = update.getMessage()
        kb = [
            [types.KeyboardButton(text="Регистрация", request_contact=True)],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
        await message.answer("Добро пожаловать в TeleMeetBot для регистрации предоставьте контакт",
                             reply_markup=keyboard)
