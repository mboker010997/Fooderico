from src.statemachine.State import State
from src.model.Update import Update
from aiogram import types
from src.statemachine.state import menu
from src import model
import logging


class StatusState(State):
    def __init__(self, context):
        super().__init__(context)
        self.nextState = self
        self.enabled = ["status_enabled", "changeStatus_enableBtn"]
        self.hidden = ["status_hidden", "changeStatus_hideBtn"]

    async def process_update(self, update: Update):
        if not update.getMessage():
            return
        text = update.getMessage().text
        if text == self.context.get_message("menuBtn"):
            self.context.set_state(menu.MenuState(self.context))
        elif text == self.context.get_message(self.enabled[1]):
            self.context.user.status = model.Status.ENABLED
        elif text == self.context.get_message(self.hidden[1]):
            self.context.user.status = model.Status.HIDDEN
        self.context.save_to_db()

    async def send_message(self, update: Update):
        if not update.getMessage():
            return

        message = update.getMessage()
        text = "Видимость анкеты: "
        current_user_status = self.context.get_message(self.context.user.status.value)

        text += current_user_status
        kb = [[types.KeyboardButton(
                    text=self.context.get_message(self.enabled[1]))],
              [types.KeyboardButton(
                    text=self.context.get_message(self.hidden[1])
                )],
              [types.KeyboardButton(
                  text=self.context.get_message("menuBtn"))],
              ]

        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb, resize_keyboard=True, one_time_keyboard=True
        )

        if self.context.user.status == model.Status.ENABLED:
            description = self.context.get_message("status_enabled_desc")
        elif self.context.user.status == model.Status.HIDDEN:
            description = self.context.get_message("status_hidden_desc")
        else:
            logging.error(f"no such user status : {self.context.user.status}")
            return

        await message.answer(text, reply_markup=types.ReplyKeyboardRemove())
        await message.answer(description, reply_markup=keyboard)
