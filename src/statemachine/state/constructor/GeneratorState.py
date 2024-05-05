from src.statemachine import State
from src.statemachine.state import search, photos, profile, menu, constructor
from src.model import Update
from aiogram import types


class GeneratorState(State):
    def __init__(self, context):
        super().__init__(context)
        self.constructorMenuBtn = context.get_message("constructorMenuBtn")

        self.nextStateDict = {
            self.constructorMenuBtn: constructor.ConstructorMenuState,
        }

    async def process_update(self, update: Update):
        if not update.get_message():
            return
        message = update.get_message()
        if message.text:
            if message.text in self.nextStateDict.keys():
                self.context.set_state(self.nextStateDict.get(message.text)(self.context))
                self.context.save_to_db()

    async def send_message(self, update: Update):
        if not update.get_message():
            return
        message = update.get_message()
        text = "Генерация меню"
        buttons = [
            [types.KeyboardButton(text=self.constructorMenuBtn)],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
        return await message.answer(text, reply_markup=keyboard)
