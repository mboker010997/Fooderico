from src.statemachine.State import State
from src.model.Update import Update
from aiogram import types
from src.statemachine.state import menu
from src.statemachine import state
from src import model
from src import bot
from src.statemachine import Context
import logging


class StatusState(State):
    def __init__(self, context):
        super().__init__(context)
        self.nextState = self
        self.enabled = ["status_enabled", "changeStatus_enableBtn"]
        self.hidden = ["status_hidden", "changeStatus_hideBtn"]
        self.disabled = ["status_disabled", "changeStatus_disableBtn"]

    def processUpdate(self, update: Update):
        if not update.getMessage():
            return
        text = update.getMessage().text
        # if self.context.user.status == model.Status.DISABLED:
        #     self.context.setState(state.InitialState())
        #     self.context.saveToDb()
        #     return
        if text == self.context.getMessage("menuBtn"):
            self.context.setState(menu.MenuState(self.context))
        elif text == self.context.getMessage(self.enabled[1]):
            self.context.user.status = model.Status.ENABLED
        elif text == self.context.getMessage(self.hidden[1]):
            self.context.user.status = model.Status.HIDDEN
        elif text == self.context.getMessage(self.disabled[1]):
            self.context.user.status = model.Status.DISABLED
        self.context.saveToDb()

    async def sendMessage(self, update: Update):
        if not update.getMessage():
            return
        message = update.getMessage()
        text = "Статус аккаунта: "
        current_user_status = self.context.getMessage(
            self.context.user.status.value
        )
        text += current_user_status
        kb = [
            [
                types.KeyboardButton(
                    text=self.context.getMessage(self.enabled[1])
                )
            ],
            [
                types.KeyboardButton(
                    text=self.context.getMessage(self.hidden[1])
                )
            ],
            [
                types.KeyboardButton(
                    text=self.context.getMessage(self.disabled[1])
                )
            ],
            [types.KeyboardButton(text=self.context.getMessage("menuBtn"))],
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb, resize_keyboard=True, one_time_keyboard=True
        )
        if self.context.user.status == model.Status.ENABLED:
            description = self.context.getMessage("status_enabled_desc")
        elif self.context.user.status == model.Status.HIDDEN:
            description = self.context.getMessage("status_hidden_desc")
        elif self.context.user.status == model.Status.DISABLED:
            description = self.context.getMessage("status_disabled_desc")
            # print(update.getChatId())
            # bot.DBController().deleteUser(update.getChatId())
            # self.context = Context()
            # return
        else:
            logging.error(f"no such user status : {self.context.user.status}")
            return
        await message.answer(text, reply_markup=types.ReplyKeyboardRemove())
        await message.answer(description, reply_markup=keyboard)
