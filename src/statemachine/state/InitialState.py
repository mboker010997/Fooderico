from State import State


class InitialState(State):
    def __init__(self, bot, dp):
        super().__init__(bot, dp)

    def processUpdate(self, message):
        pass

    def getNextState(self, message):
        return InitialState(self.bot, self.dp)
    
    async def sendMessage(self, message):
        await message.answer("Initial State")
