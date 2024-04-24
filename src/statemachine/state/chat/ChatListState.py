from src.statemachine import State
from src.model import Update
from src import bot
from aiogram import types
from src.statemachine.state import menu


class ChatListState(State):
    def __init__(self, context):
        super().__init__(context)

    async def process_update(self, update: Update):
        print("in chat list")
        pass

    async def __switchContext(self, update: Update):
        self.context.set_state(menu.MenuState(self.context))
        self.context.save_to_db()
        await self.context.state.send_message(update)

    async def send_message(self, update: Update):
        if not update.get_message():
            return
        message = update.get_message()

        list_of_matches = bot.DBController().get_user_matches_ids(self.context.user.id)
        list_of_user_ids = [user_id[0] for user_id in list_of_matches]
        print('===============CHATLISTSTATE', list_of_matches)
        print('===============CHATLISTSTATE', list_of_user_ids)

        if not list_of_user_ids:
            await message.answer(self.context.get_message("chat_no_match"))
        for user_id in list_of_user_ids:
            await self.__send_match(update, user_id, self.context.user.id)
        await self.__switchContext(update)

    @staticmethod
    async def __send_match(update, from_user_id, to_user_id):
        from_user = bot.DBController().get_user(from_user_id)
        to_user = bot.DBController().get_user(to_user_id)

        text = f"{from_user.profile_name}\n{from_user.about}"
        send_contacts_button = types.InlineKeyboardButton(
            text="Анонимный чат",
            callback_data=f"go_anon_chat_{from_user.chat_id}",
        )
        send_contacts_keyboard = types.InlineKeyboardMarkup(
            inline_keyboard=[[send_contacts_button]]
        )

        if from_user.photo_file_ids:
            await update.bot.send_photo(
                chat_id=to_user.chat_id,
                photo=from_user.photo_file_ids[0],
                caption=text,
                reply_markup=send_contacts_keyboard,
            )
        else:
            await update.bot.send_message(
                chat_id=to_user.chat_id,
                text=text,
                reply_markup=send_contacts_keyboard,
            )
