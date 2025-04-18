from src.statemachine import State
from src.model import Update
from src import bot, model
from src.statemachine.state import menu
from aiogram import types
import re


class OtherInterests(State):
    def __init__(self, context):
        super().__init__(context)
        self.state = None
        self.is_updating = False
        self.addBtn = self.context.get_message("addBtn")
        self.deleteBtn = self.context.get_message("deleteBtn")
        self.continueBtn = self.context.get_message("continueBtn")

    def update_tags(self, tags):
        if self.state == "add":
            self.context.user.others_interests += " " + tags
        else:
            tmp = re.split(r"[ ,]+", tags)
            self.context.user.others_interests = " ".join(
                [tag for tag in self.context.user.others_interests.split() if tag not in tmp]
            )

    async def process_update(self, update: Update):
        if not update.get_message():
            return
        message = update.get_message()
        if self.is_updating:
            self.update_tags(message.text)
            self.is_updating = False
        else:
            if message.text == self.addBtn:
                self.state = "add"
                self.is_updating = True
            elif message.text == self.deleteBtn:
                self.state = "delete"
                self.is_updating = True
            elif message.text == self.continueBtn:
                self.context.set_state(menu.MenuState(self.context))
                self.is_updating = True
                self.context.user.status = model.Status.ENABLED
        self.context.save_to_db()

    async def send_message(self, update: Update):
        if not update.get_message():
            return
        message = update.get_message()
        buttons = [
            [types.KeyboardButton(text=self.context.get_message("addBtn"))],
            [types.KeyboardButton(text=self.context.get_message("deleteBtn"))],
            [types.KeyboardButton(text=self.context.get_message("continueBtn"))],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
        if self.is_updating:
            if self.state == "add":
                await message.answer(self.context.get_message("add_interests"))
            elif self.state == "delete":
                await message.answer(self.context.get_message("delete_interests"))
        else:
            await message.answer(
                "Ваши интересы: "
                + (
                    bot.DBController().get_user(self.context.user.id).others_interests
                    or self.context.get_message("empty_interests")
                ),
                reply_markup=keyboard,
            )
