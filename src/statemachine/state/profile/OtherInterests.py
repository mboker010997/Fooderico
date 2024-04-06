from src.statemachine import State
from src.model import Update
from src.statemachine.state import menu
from aiogram import types


class OtherInterests(State):
    def __init__(self, context):
        super().__init__(context)
        self.state = None
        self.is_updating = False
        self.addBtn = self.context.getMessage("addBtn")
        self.deleteBtn = self.context.getMessage("deleteBtn")
        self.continueBtn = self.context.getMessage("continueBtn")
    

    def updateTags(self, tags):
        if (self.state == "add"):
            self.context.user.others_interests += tags + " "
        else:
            self.context.user.others_interests = \
            ' '.join([tag for tag in self.context.user.others_interests.split() if tag not in tags.split()])

    def processUpdate(self, update: Update):
        if not update.getMessage():
            return
        message = update.getMessage()
        if self.is_updating:
            self.updateTags(message.text)
            self.is_updating = False
        else:
            if message.text == self.addBtn:
                self.state = "add"
                self.is_updating = True
            elif message.text == self.deleteBtn:
                self.state = "delete"
                self.is_updating = True
            elif message.text == self.continueBtn:
                self.context.setState(menu.MenuState(self.context))
                self.context.saveToDb()
                self.is_updating = True

        
    async def sendMessage(self, update: Update):
        if not update.getMessage():
            return
        message = update.getMessage()
        kb = [
            [types.KeyboardButton(text=self.context.getMessage("addBtn"))],
            [types.KeyboardButton(text=self.context.getMessage("deleteBtn"))],
            [types.KeyboardButton(text=self.context.getMessage("continueBtn"))],
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb, resize_keyboard=True
        )
        if self.is_updating:
            if self.state == "add":
                await message.answer(self.context.getMessage("add_interests"))
            elif self.state == "delete":
                await message.answer(self.context.getMessage("delete_interests"))
        else:
            await message.answer("Ваши интересы: " + self.context.user.others_interests, reply_markup=keyboard)
