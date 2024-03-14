from src.statemachine.State import State
from src.statemachine.state.profile.AgeState import AgeState
from aiogram import types, Bot, Dispatcher
from src.bot.Update import Update


class UsernameState(State):
    def __init__(self):
        super().__init__()

    def processUpdate(self, update: Update):
        pass

    def getNextState(self, update: Update):
        return AgeState()

    async def sendMessage(self, update: Update):
        message = update.getMessage()
        kb = [
            [types.KeyboardButton(text="Оставь текущее")],
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb, resize_keyboard=True, one_time_keyboard=True
        )
        await message.answer("Введите имя", reply_markup=keyboard)