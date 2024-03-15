from src.statemachine.State import State
from src.bot.Update import Update
from aiogram import types
import src.statemachine.state.menu as menu


class StatusState(State):
    def __init__(self):
        super().__init__()
        self.nextState = self
        self.enabled = ["Активен", "Активировать"]
        self.hidden = ["Скрыт", "Спрятать"]
        self.disabled = ["Отключен", "Отключить"]
        self.menuBtn = "Вернуться в меню"

    def processUpdate(self, update: Update):
        text = update.getMessage().text
        if text == self.menuBtn:
            self.nextState = menu.MenuState()

    def getNextState(self, update: Update):
        return self.nextState

    async def sendMessage(self, update: Update):
        message = update.getMessage()
        text = "Статус аккаунта: "
        # text += current_user_status
        kb = [
            [types.KeyboardButton(text=self.enabled[1])],
            [types.KeyboardButton(text=self.hidden[1])],
            [types.KeyboardButton(text=self.disabled[1])],
            [types.KeyboardButton(text=self.menuBtn)],
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb, resize_keyboard=True, one_time_keyboard=True
        )
        await message.answer(text, reply_markup=keyboard)
