from src.statemachine.State import State
from aiogram import types
from src.statemachine.state.profile.AboutState import AboutState


class GeoState(State):
    def __init__(self):
        super().__init__()
        self.steps = 0
        self.STEPS_COUNT = 5

    def processUpdate(self, message: types.Message):
        pass

    def getNextState(self, message):
        return

    async def sendMessage(self, message, bot, dp):
        kb = [
            [types.KeyboardButton(
                text="Передать геолокацию",
                request_location=True,
            )],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, one_time_keyboard=True)
        await message.answer("Передайте геолокацию или укажите город",
                             reply_markup=keyboard)
