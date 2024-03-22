from src.statemachine import State
from src.statemachine.state.registration import RegisterState
from src.model import Update
from src.statemachine import Context


class InitialState(State):
    def __init__(self):
        super().__init__()

    async def sendMessage(self, update: Update):
        pass

    def processUpdate(self, update: Update):
        message = update.getMessage()
        lang_code = message.from_user.language_code
        self.context = Context(lang_code)

        self.context.user.chat_id = update.getChatId()
        self.context.user.language_code = lang_code
        self.context.username = message.from_user.username

        self.context.setState(RegisterState(self.context))
        self.context.saveToDb()
