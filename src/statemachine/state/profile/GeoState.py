from src.statemachine.State import State
from aiogram import types
from src.statemachine.state import profile
from src.model import Update


class GeoState(State):
    def __init__(self, context):
        super().__init__(context)

    def processUpdate(self, update: Update):
        message = update.getMessage()
        if message.location:
            # todo(mboker0109): FOOD-44
            pass
        else:
            # todo(mboker0109): FOOD-44
            pass
        self.context.setState(profile.AboutState(self.context))
        self.context.saveToDb()

    async def sendMessage(self, update: Update):
        chatId = update.getChatId()
        kb = [
            [types.KeyboardButton(
                text="Передать геолокацию",
                request_location=True,
            )],
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb, resize_keyboard=True, one_time_keyboard=True
            )
        await update.bot.send_message(chat_id=chatId, text="Передайте геолокацию или укажите город",
                             reply_markup=keyboard)
