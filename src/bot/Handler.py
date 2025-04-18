from aiogram import types
from src.model.Update import Update, Message, PollAnswer, CallbackQuery
import logging
from src.model import StateUpdater
from typing import List
from aiogram import F
from aiogram.types import (
    ContentType as CT,
    Message as mes,
)
from src.statemachine.state import chat
from src import bot


class Handler:
    def __init__(self, telebot: bot.TelegramBot):
        self.bot = telebot.bot
        self.dp = telebot.dp
        self.message_storage = telebot.message_storage
        self.telebot = telebot
        self.register_handlers()

    async def update_handler(self, update: Update):
        chat_id = update.get_chat_id()
        sentMessage = StateUpdater.get_sent_message(chat_id)
        # print(sentMessage)
        if sentMessage is not None and not sentMessage.text.startswith('Генерация меню'):
            await self.bot.delete_message(chat_id=sentMessage.chat.id, message_id=sentMessage.message_id)

        try:
            curState = StateUpdater.get_state(chat_id)
            nextState = await curState.go_next_state(update)
            newMessage = await nextState.send_message(update)
            StateUpdater.set_sent_message(chat_id, newMessage)
        except Exception as exc:
            logging.exception("Handler")
            logging.exception(exc)
            admins = bot.DBController().get_all_admins()
            for id in admins:
                await self.bot.send_message(id, f"An error occurred in Handler: {exc}")

    def register_handlers(self):
        @self.dp.message(F.content_type.in_([CT.PHOTO]))
        async def handle_albums(message: mes, album: List[mes] = None):
            update = Message(self.telebot, message)
            update.album = album
            await self.update_handler(update)

        @self.dp.message(F.content_type.in_([CT.VIDEO_NOTE]))
        async def handle_video_note(message: mes):
            update = Message(self.telebot, message)
            update.video_note_id = message.video_note.file_id
            await self.update_handler(update)

        @self.dp.message(F.content_type.in_([CT.VOICE]))
        async def handle_voice(message: mes):
            update = Message(self.telebot, message)
            update.voice_id = message.voice.file_id
            await self.update_handler(update)

        @self.dp.poll_answer()
        async def poll_answer_handler(poll: types.PollAnswer):
            update = PollAnswer(self.telebot, poll)
            await self.update_handler(update)

        @self.dp.message()
        async def message_handler(message: mes):
            update = Message(self.telebot, message)
            await self.update_handler(update)

        @self.dp.callback_query(F.data.startswith("go_anon_chat_"))
        async def transition_to_anon_chat(callback: types.CallbackQuery):
            chat_id = callback.from_user.id
            update = CallbackQuery(self.telebot, callback)
            context = StateUpdater.get_context(chat_id)
            if context is None:
                return

            expected_prefix = "go_anon_chat_"
            other_chat_id = int(callback.data[len(expected_prefix):])
            context.other_chat_id = other_chat_id
            context.set_state(chat.ChatState(context))
            context.save_to_db()

            await context.state.send_message(update)

        @self.dp.callback_query(F.data.startswith("delete_photo_"))
        async def delete_photo_handler(callback: types.CallbackQuery):
            chat_id = callback.from_user.id
            update = CallbackQuery(self.telebot, callback)
            context = StateUpdater.get_context(chat_id)
            if context is None:
                return
            print(callback.data)
            parts = callback.data.split("_")
            idx = parts[2]
            user = context.user
            photo_ids = user.photo_file_ids
            photo_id = photo_ids[int(idx)]
            photo_ids.remove(photo_id)
            context.save_to_db()
            await context.state.send_message(update)
            await callback.answer()

        @self.dp.callback_query(F.data.startswith("choose_main_photo_"))
        async def main_photo_handler(callback: types.CallbackQuery):
            chat_id = callback.from_user.id
            update = CallbackQuery(self.telebot, callback)
            context = StateUpdater.get_context(chat_id)
            if context is None:
                return

            print(callback.data)
            parts = callback.data.split("_")
            idx = parts[3]
            user = context.user
            photo_ids = user.photo_file_ids
            i, j = 0, int(idx)
            photo_ids[i], photo_ids[j] = photo_ids[j], photo_ids[i]
            context.save_to_db()
            await context.state.send_message(update)
            await callback.answer()

        async def relation_handler(callback: types.CallbackQuery, relation):
            chat_id = callback.from_user.id
            update = CallbackQuery(self.telebot, callback)
            context = StateUpdater.get_context(chat_id)
            if context is None:
                return
            parts = callback.data.split("_")
            idx = parts[3]
            user = context.user
            query = f"SELECT * FROM tele_meet_relations WHERE user_id = {user.id};"
            bot.DBController().cursor.execute(query)
            self.other_user_rows = bot.DBController().cursor.fetchall()
            num = int(idx)
            other_user_id = self.other_user_rows[num][2]
            if relation == "FOLLOW":
                bot.DBController().cursor.execute(
                    f"SELECT * FROM tele_meet_relations "
                    f"WHERE "
                    f"user_id = {other_user_id} AND other_user_id = {user.id} AND relation = 'FOLLOW';"
                )
                rows = bot.DBController().cursor.fetchall()
                print(rows)
                if rows and len(rows) > 0:
                    my_user = bot.DBController().get_user(user.id)
                    other_user = bot.DBController().get_user(other_user_id)
                    cursor = bot.DBController().cursor
                    cursor.execute(
                        f"INSERT INTO tele_meet_match (user_id, other_user_id) VALUES ({user.id}, {other_user_id})"
                    )
                    cursor.execute(
                        f"INSERT INTO tele_meet_match (user_id, other_user_id) VALUES ({other_user_id}, {user.id})"
                    )
                    await __send_match(update, my_user, other_user)
                    await __send_match(update, other_user, my_user)

            bot.DBController().cursor.execute(
                f"UPDATE tele_meet_relations "
                f"SET relation = '{relation}' "
                f"WHERE "
                f"user_id = {user.id} AND other_user_id = {other_user_id};"
            )
            context.save_to_db()
            await context.state.send_message(update)
            await callback.answer()

        async def __send_match(update, from_user, to_user):
            text = (
                f"Вас лайкнул в ответ: {from_user.profile_name}\n{from_user.about}"
            )

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

        @self.dp.callback_query(F.data.startswith("change_to_like_"))
        async def change_to_like_callback_handler(
            callback: types.CallbackQuery,
        ):
            await relation_handler(callback, "FOLLOW")

        @self.dp.callback_query(F.data.startswith("change_to_skip_"))
        async def change_to_skip_callback_handler(
            callback: types.CallbackQuery,
        ):
            await relation_handler(callback, "SKIPPED")

        @self.dp.callback_query(F.data.startswith("change_to_dislike_"))
        async def change_to_dislike_callback_handler(
            callback: types.CallbackQuery,
        ):
            await relation_handler(callback, "BLACKLIST")

        @self.dp.callback_query(F.data.startswith("remove_"))
        async def remove_relation_callback_handler(
            callback: types.CallbackQuery,
        ):
            chat_id = callback.from_user.id
            update = CallbackQuery(self.telebot, callback)
            context = StateUpdater.get_context(chat_id)
            if context is None:
                return
            parts = callback.data.split("_")
            idx = parts[1]
            user = context.user
            query = f"SELECT * FROM tele_meet_relations WHERE user_id = {user.id};"
            bot.DBController().cursor.execute(query)
            self.other_user_rows = bot.DBController().cursor.fetchall()
            num = int(idx)
            other_user_id = self.other_user_rows[num][2]
            bot.DBController().cursor.execute(
                f"DELETE FROM tele_meet_relations WHERE " f"user_id = {user.id} AND other_user_id = {other_user_id};"
            )
            context.save_to_db()
            await context.state.send_message(update)
            await callback.answer()
