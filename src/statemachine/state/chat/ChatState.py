from src.statemachine import State
from src.model import Update
from src import bot
from aiogram import types
from src.statemachine.state import menu


class ChatState(State):
    def __init__(self, context):
        super().__init__(context)
        self.other_chat_id = self.context.other_chat_id

    def processUpdate(self, update: Update):
        if not update.getMessage():
            return
        text = update.getMessage().text
        if text == self.context.getMessage("menuBtn"):
            self.context.setState(menu.MenuState(self.context))
        # else:
        #     bot.send_message(self.other_chat_id, text)
        self.context.saveToDb()

    async def sendMessage(self, update: Update):
        # if not update.getMessage():
        #     return
        callback = update.getCallbackQuery()
        other_user = bot.DBController().getUserByChatId(self.other_chat_id)
        kb = [
            [types.KeyboardButton(text=self.context.getMessage("menuBtn"))],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
        await callback.message.answer(f"Вы попали в анонимный чат с {other_user.profile_name}", reply_markup=keyboard)
        await callback.answer()
