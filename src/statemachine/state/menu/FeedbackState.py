from src.statemachine import State
from src.model import Update
from src.statemachine.state import menu
from src import bot


class FeedbackState(State):
    def __init__(self, context):
        super().__init__(context)

    async def process_update(self, update: Update):
        if not update.get_message():
            return
        message = update.get_message()

        if message.text:
            admins = bot.DBController().get_all_admins()
            for id in admins:
                await update.bot.send_message(
                    chat_id=id,
                    text=message.text,
                )
                # await bot.TelegramBot.bot.send_message(id, message.text)

        self.context.set_state(menu.MenuState(self.context))
        self.context.save_to_db()

    async def send_message(self, update: Update):
        if not update.get_message():
            return
        message = update.get_message()

        await message.answer(self.context.get_message("feedback_text"))
