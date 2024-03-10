from src.statemachine.State import State
from src.statemachine.state.registration.RegisterState import RegisterState


class InitialState(State):
    def __init__(self):
        super().__init__()

    def processUpdate(self, message):
        pass

    def getNextState(self, message):
        return RegisterState()

    async def sendMessage(self, message, bot, dp):
        await message.answer("Initial State")
