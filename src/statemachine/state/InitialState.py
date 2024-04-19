from src.statemachine import State
from src.statemachine.state.registration import RegisterState
from src.model import Update
from src import model
from src.statemachine import Context


class InitialState(State):
    def __init__(self, context=Context()):
        super().__init__()
        self.context = context

    async def send_message(self, update: Update):
        pass

    async def process_update(self, update: Update):
        if not update.getMessage():
            return
        message = update.getMessage()
        lang_code = message.from_user.language_code
        self.context = Context(lang_code)

        self.context.user.chat_id = update.getChatId()
        self.context.user.language_code = lang_code
        self.context.user.username = message.from_user.username
        self.context.user.others_interests = ""
        self.context.user.status = model.Status.HIDDEN

        self.context.set_state(RegisterState(self.context))
        self.context.save_to_db()
