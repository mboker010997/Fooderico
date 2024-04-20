from src.statemachine import State
from src.model import Update
from src import bot
from aiogram import types
from src.statemachine.state import menu
from aiogram import types


class ChatState(State):
    def __init__(self, context):
        super().__init__(context)
        self.other_chat_id = self.context.other_chat_id
        self.share_contacts = False
        self.first_entered = True

    async def process_update(self, update: Update):
        self.first_entered = False
        if update.get_message().text == "Выйти из чата":
            await update.message_storage.close(update.get_chat_id(), self.other_chat_id)
            self.context.set_state(menu.MenuState(self.context))
            self.context.save_to_db()
        elif update.get_message().text == "Поделиться контактами":
            self.share_contacts = True
        else:
            message = update.get_message()
            if message is not None:
                self.text = message.text

    async def send_message(self, update: Update):
        # if not update.get_message():
        #     return

        callback = update.get_callback_query()
        chat_id = update.get_chat_id()
        user = bot.DBController().getUserByChatId(update.get_chat_id())
        other_user = bot.DBController().getUserByChatId(self.other_chat_id)
        if self.first_entered:
            kb = [
                [types.KeyboardButton(text="Выйти из чата")],
                [types.KeyboardButton(text="Поделиться контактами")],
            ]
            keyboard = types.ReplyKeyboardMarkup(
                keyboard=kb, resize_keyboard=True, one_time_keyboard=True
            )
            await callback.message.answer(
                f"Вы попали в анонимный чат с {other_user.profile_name}",
                reply_markup=keyboard,
            )
            await update.message_storage.open(chat_id, self.other_chat_id)
            delayed_messages = await update.message_storage.dump_messages(self.other_chat_id, chat_id)
            for message in delayed_messages:
                await callback.message.answer(message)
        else:
            is_closed = await update.message_storage.is_closed(self.other_chat_id, chat_id)
            if is_closed:
                await update.message_storage.put_message(chat_id, self.other_chat_id, self.text)
            else:
                await update.bot.send_message(chat_id=self.other_chat_id, text=self.text)

        if self.share_contacts:
            self.share_contacts = False
            my_info, my_is_link = self.__generate_telegram_user_link(
                user.username, user.phone_number
            )
            text = "С вами поделились контактами: {}\n".format(
                user.profile_name
            )
            text += (
                "Ссылка на этого пользователя - {}\n".format(my_info)
                if my_is_link
                else "Номер этого пользователя - {}\n".format(my_info)
            )
            await update.bot.send_message(
                chat_id=self.other_chat_id, text=text
            )
        if callback is not None:
            await callback.answer()

    @staticmethod
    def __generate_telegram_user_link(username, phone_number):
        if username:
            return (f"https://t.me/{username}", True)
        else:
            return (phone_number, False)
