from src.statemachine.State import State
from src.model.Update import Update
from aiogram import types
from src.statemachine.state import menu, profile


class ShowProfileState(State):
    def __init__(self, context):
        super().__init__(context)
        self.edit = "Редактировать"
        self.menu = "Вернуться в меню"
        self.nextState = self

    def processUpdate(self, update: Update):
        answer = update.getMessage().text
        if answer == self.edit:
            self.context.setState(profile.UsernameState(self.context))
            self.context.saveToDb()
        elif answer == self.menu:
            self.context.setState(menu.MenuState(self.context))
            self.context.saveToDb()

    async def sendMessage(self, update: Update):
        message = update.getMessage()
        text = "Ваш профиль:\n"
        # text += user.toString() # implement toString for user class
        # embed user field into all states
        kb = [
            [types.KeyboardButton(text=self.edit)],
            [types.KeyboardButton(text=self.menu)],
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb, resize_keyboard=True, one_time_keyboard=True
        )
        await message.answer(text, reply_markup=keyboard)
