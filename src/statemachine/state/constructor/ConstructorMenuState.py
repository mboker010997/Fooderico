from src.statemachine import State
from src.statemachine.state import menu, constructor
from src.model import Update
from aiogram import types


class ConstructorMenuState(State):
    def __init__(self, context):
        super().__init__(context)
        self.generateBtn = context.get_message("constructor_menu_generateBtn")
        self.addDietsBtn = context.get_message("constructor_menu_addDietsBtn")
        self.menuBtn = context.get_message("menuBtn")

        self.nextStateDict = {
            self.generateBtn: constructor.GeneratorState,
            self.addDietsBtn: constructor.DietState,
            self.menuBtn: menu.MenuState,
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
        text = "Конструктор меню"
        buttons = [
            [types.KeyboardButton(text=self.generateBtn)],
            [types.KeyboardButton(text=self.addDietsBtn)],
            [types.KeyboardButton(text=self.menuBtn)],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
        return await message.answer(text, reply_markup=keyboard)
