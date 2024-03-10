from src.statemachine.State import State
from aiogram import types
from src.statemachine.state.profile.GeoState import GeoState


class InterestsTagState(State):
    def __init__(self):
        super().__init__()

    def processUpdate(self, message: types.Message):
        pass

    def getNextState(self, message):
        return GeoState()

    async def sendMessage(self, message, bot, dp):
        await message.answer("Какие у вас интересы?")
