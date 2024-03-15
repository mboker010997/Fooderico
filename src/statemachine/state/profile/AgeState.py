from src.statemachine.State import State
from src.statemachine.state.profile.GenderState import GenderState
from aiogram import Bot, Dispatcher
from src.bot.Update import Update


class AgeState(State):
    def __init__(self):
        super().__init__()

    def processUpdate(self, update: Update):
        pass

    def getNextState(self, update: Update):
        return GenderState()

    async def sendMessage(self, update: Update):
        message = update.getMessage()
        await message.answer("Введите возраст")
