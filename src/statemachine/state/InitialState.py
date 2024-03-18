from src.statemachine import State
from src.statemachine.state.registration import RegisterState
from src.model import Update
from src.statemachine import Context


class InitialState(State):
    def __init__(self):
        super().__init__(Context())

    async def sendMessage(self, update: Update):
        pass

    def processUpdate(self, update: Update):
        message = update.getMessage()
        self.context.user.chat_id = update.getChatId()
        self.context.username = message.from_user.username

        self.context.setState(RegisterState(self.context))
        self.context.saveToDb()
