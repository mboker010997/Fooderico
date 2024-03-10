from src.statemachine.State import State
from src.statemachine.state.profile.AgeState import AgeState
from aiogram import types


class UsernameState(State):
    def __init__(self):
        super().__init__()

    def processUpdate(self, message):
        pass

    def getNextState(self, message):
        return AgeState()

    async def sendMessage(self, message: types.Message, bot, dp):
        kb = [
            [types.KeyboardButton(text="Оставь текущее")],
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb, resize_keyboard=True, one_time_keyboard=True
        )
        await message.answer("Введите имя", reply_markup=keyboard)