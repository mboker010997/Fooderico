from src.statemachine.State import State
from src.statemachine.state.profile.RestrictionsTagState import RestrictionsTagState
from aiogram import types
from src.bot.Update import Update


class GenderState(State):
    def __init__(self):
        super().__init__()

    def processUpdate(self, update: Update):
        message = update.getMessage()
        if message.text != "Мужской" and message.text != "Женский":
            self.nextState = self
        else:
            self.nextState = RestrictionsTagState()

    def getNextState(self, update: Update):
        return self.nextState

    async def sendMessage(self, update: Update):
        message = update.getMessage()
        kb = [
            [types.KeyboardButton(text="Мужской")],
            [types.KeyboardButton(text="Женский")],
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb, resize_keyboard=True, one_time_keyboard=True
        )
        await message.answer("Какой у вас пол?", reply_markup=keyboard)
