from src.statemachine.State import State
from src.bot.Update import Update
from aiogram import types
import src.statemachine.state.menu as menu
from src.statemachine.state.profile.UsernameState import UsernameState
import logging


class ShowProfileState(State):
    def __init__(self):
        super().__init__()
        self.edit = "Редактировать"
        self.menu = "Вернуться в меню"
        self.nextState = self

    def processUpdate(self, update: Update):
        answer = update.getMessage().text
        if answer == self.edit:
            self.nextState = UsernameState()
        elif answer == self.menu:
            self.nextState = menu.MenuState()

    def getNextState(self, update: Update):
        return self.nextState

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
