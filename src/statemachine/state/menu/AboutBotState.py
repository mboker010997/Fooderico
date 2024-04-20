from src.statemachine import State
from src.model import Update
from src.statemachine.state import menu
from aiogram.enums import ParseMode


class AboutBotState(State):
    def __init__(self, context):
        super().__init__(context)

    async def process_update(self, update: Update):
        pass

    async def send_message(self, update: Update):
        if not update.get_message():
            return

        message = update.get_message()
        await message.answer(
            self.context.get_message("aboutBot_text"), parse_mode=ParseMode.HTML
        )

        self.context.set_state(menu.MenuState(self.context))
        self.context.save_to_db()
        menu_state = menu.MenuState(self.context)
        await menu_state.send_message(update)
