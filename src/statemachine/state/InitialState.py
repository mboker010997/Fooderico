from State import State


class InitialState(State):
    def __init__(self):
        super().__init__()

    async def processUpdate(self):
        pass

    async def parseInput(self, message):
        await message.answer("mbombo")