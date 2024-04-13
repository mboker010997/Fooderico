from src.statemachine import State
from src.model import Update
from src import bot
from src.statemachine.state import menu


class ChatState(State):
    def __init__(self, context):
        super().__init__(context)
        self.other_chat_id = self.context.other_chat_id

    def processUpdate(self, update: Update):
        self.context.setState(menu.MenuState(self.context))
        self.context.saveToDb()

    async def sendMessage(self, update: Update):
        callback = update.getCallbackQuery()
        other_user = bot.DBController().getUserByChatId(self.other_chat_id)
        await callback.message.answer(f"Вы попали в анонимный чат с {other_user.profile_name}")
        await callback.answer()
