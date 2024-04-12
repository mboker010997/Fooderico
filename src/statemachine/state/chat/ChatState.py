from src.statemachine import State
from src.model import Update
from src import bot
from src.statemachine.state import menu
from aiogram import types


class ChatState(State):
    def __init__(self, context):
        super().__init__(context)
        self.other_chat_id = self.context.other_chat_id
        self.share_contacts = False

    def processUpdate(self, update: Update):
        if update.getMessage().text == "Выйти из чата":
            self.context.setState(menu.MenuState(self.context))
            self.context.saveToDb()
        elif update.getMessage().text == "Поделиться контактами":
            self.share_contacts = True

    async def sendMessage(self, update: Update):
        callback = update.getCallbackQuery()

        user = bot.DBController().getUserByChatId(update.getChatId())
        other_user = bot.DBController().getUserByChatId(self.other_chat_id)
        if self.share_contacts:
            self.share_contacts = False
            my_info, my_is_link = self.__generate_telegram_user_link(user.username, user.phone_number)
            text = "С вами поделились контактамт: {}\n".format(user.profile_name)
            text += "Ссылка на этого пользователя - {}\n".format(my_info) if my_is_link else "Номер этого пользователя - {}\n".format(my_info)
            await update.bot.send_message(chat_id=self.other_chat_id, text=text)
        kb = [
            [types.KeyboardButton(text="Выйти из чата")],
            [types.KeyboardButton(text="Поделиться контактами")]
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb, resize_keyboard=True, one_time_keyboard=True
        )
        await callback.message.answer(f"Вы попали в анонимный чат с {other_user.profile_name}", keyboard=keyboard)
        await callback.answer()

    @staticmethod
    def __generate_telegram_user_link(username, phone_number):
        if username:
            return (f'https://t.me/{username}', True)
        else:
            return (phone_number, False)