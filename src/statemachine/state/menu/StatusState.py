from src.statemachine.State import State
from src.model.Update import Update
from aiogram import types
from src.statemachine.state import menu
from src import model


class StatusState(State):
    def __init__(self, context):
        super().__init__(context)
        self.nextState = self
        self.enabled = ["Активен", "Активировать"]
        self.hidden = ["Скрыт", "Спрятать"]
        self.disabled = ["Отключен", "Отключить"]
        self.menuBtn = "Вернуться в меню"

    def processUpdate(self, update: Update):
        text = update.getMessage().text
        if text == self.menuBtn:
            self.context.setState(menu.MenuState(self.context))
        elif text == self.enabled[1]:
            self.context.user.status = model.Status.ENABLED
        elif text == self.hidden[1]:
            self.context.user.status = model.Status.HIDDEN
        elif text == self.disabled[1]:
            self.context.user.status = model.Status.DISABLED
        self.context.saveToDb()

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
