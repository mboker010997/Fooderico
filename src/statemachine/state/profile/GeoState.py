from src.statemachine.State import State
from aiogram import types
import src.statemachine.state.profile as profile
from src.bot.Update import Update


class GeoState(State):
    def __init__(self):
        super().__init__()

    def processUpdate(self, update: Update):
        pass

    def getNextState(self, update: Update):
        return profile.AboutState()

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
