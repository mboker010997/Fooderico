from src.statemachine.State import State
from aiogram import types


class AboutState(State):
    def __init__(self):
        super().__init__()

    def processUpdate(self, message: types.Message):
        pass

    def getNextState(self, message):
        pass

    async def sendMessage(self, message, bot, dp):
        await message.answer("Напишите информацию о себе")
