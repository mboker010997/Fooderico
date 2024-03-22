from src.statemachine import State
from src.statemachine.state import profile
from src.model import Update


class AgeState(State):
    def __init__(self, context):
        super().__init__(context)
        self.text = self.context.getMessage("age_text")

    def processUpdate(self, update: Update):
        message = update.getMessage()
        if message.text.isdigit() and (int(message.text) in range(1, 100)):
            self.context.user.age = int(message.text)
            self.context.setState(profile.GenderState(self.context))
            self.context.saveToDb()
        else:
            self.text = self.context.getMessage("age_parsing_error")

    async def sendMessage(self, update: Update):
        message = update.getMessage()
        await message.answer(self.text)
