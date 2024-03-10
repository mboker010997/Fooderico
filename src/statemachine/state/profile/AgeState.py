from src.statemachine.State import State
from src.statemachine.state.profile.GenderState import GenderState


class AgeState(State):
    def __init__(self):
        super().__init__()

    def processUpdate(self, message):
        pass

    def getNextState(self, message):
        return GenderState()

    async def sendMessage(self, message, bot, dp):
        await message.answer("Введите возраст")
