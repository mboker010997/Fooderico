from src.statemachine import State
from src.model import Update
from src import bot
from aiogram import types
from src.statemachine.state import menu


class ChatListState(State):
    def __init__(self, context):
        super().__init__(context)

    def processUpdate(self, update: Update):
        self.context.setState(menu.MenuState(self.context))
        self.context.saveToDb()

    async def sendMessage(self, update: Update):
        if not update.getMessage():
            return
        counter = 0
        message = update.getMessage()

        list_of_matches = bot.DBController().getUserRelationsIds(self.context.user.id)  ###
        list_of_user_ids = [user_id[0] for user_id in list_of_matches]

        if not list_of_user_ids:
            await message.answer(self.context.getMessage("Список чатов пуст"))
        for user_id in list_of_user_ids:
            await self.__send_match(update, user_id, self.context.user.id)

    @staticmethod
    async def __send_match(update, from_user_id, to_user_id):
        from_user = bot.DBController().getUser(from_user_id)
        to_user = bot.DBController().getUser(to_user_id)

        text = f"{from_user.profile_name}\n{from_user.about}"
        send_contacts_button = types.InlineKeyboardButton(text='Анонимный чат',
                                                          callback_data=f'go_anon_chat_{from_user.chat_id}')
        send_contacts_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [send_contacts_button]
        ])

        if from_user.photo_file_ids:
            await update.bot.send_photo(chat_id=to_user.chat_id,
                                        photo=from_user.photo_file_ids[0],
                                        caption=text,
                                        reply_markup=send_contacts_keyboard)
        else:
            await update.bot.send_message(chat_id=to_user.chat_id,
                                          text=text,
                                          reply_markup=send_contacts_keyboard)
