from src.statemachine.State import State
from src.statemachine.state.profile.GenderState import GenderState
from src.bot.Update import Update


class AgeState(State):
    def __init__(self):
        super().__init__()
        self.text = "Введите возраст"

    def processUpdate(self, update: Update):
        message = update.getMessage()
        if message.text.isdigit() and (int(message.text) in range(1, 100)):
            self.nextState = GenderState()
        else:
            self.text = "Возраст должен быть числом от 1 до 99"
            self.nextState = self

    def getNextState(self, update: Update):
        return self.nextState

    async def sendMessage(self, update: Update):
        message = update.getMessage()
        await message.answer(self.text)
