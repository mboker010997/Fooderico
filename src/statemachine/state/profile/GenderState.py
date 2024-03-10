from src.statemachine.State import State
from aiogram import types
from src.statemachine.state.profile.RestrictionsTagState import RestrictionsTagState


class GenderState(State):
    def __init__(self):
        super().__init__()

    def processUpdate(self, message: types.Message):
        if message.text != "Мужской" and message.text != "Женский":
            self.nextState = self
        else:
            self.nextState = RestrictionsTagState()

    def getNextState(self, message):
        return self.nextState

    async def sendMessage(self, message, bot, dp):
        kb = [
            [types.KeyboardButton(text="Мужской")],
            [types.KeyboardButton(text="Женский")],
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb, resize_keyboard=True, one_time_keyboard=True
        )
        await message.answer("Какой у вас пол?", reply_markup=keyboard)
