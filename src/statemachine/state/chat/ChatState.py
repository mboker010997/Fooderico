from src.statemachine import State
from src import bot
from aiogram import types
from src.statemachine.state import menu
from src.statemachine.state import chat
from src.model import Update, Tags as tags


class ChatState(State):
    def __init__(self, context):
        super().__init__(context)
        self.other_chat_id = self.context.other_chat_id
        self.share_contacts = False
        self.first_entered = True

    async def process_update(self, update: Update):
        self.first_entered = False
        if update.video_note_id:
            self.text = [update.video_note_id, "video_note"]
        elif update.voice_id:
            self.text = [update.voice_id, "voice"]
        elif update.get_message().text == "Выйти из чата":
            await update.message_storage.close(update.get_chat_id(), self.other_chat_id)
            self.context.set_state(menu.MenuState(self.context))
            self.context.save_to_db()
        elif update.get_message().text == "Поделиться контактами":
            self.share_contacts = True
        elif update.get_message().text == "Пожаловаться на собеседника":
            await update.message_storage.close(update.get_chat_id(), self.other_chat_id)
            photo_id, complaint_text = await self.get_complaint_text(update)
            self.context.set_state(chat.ComplaintState(self.context, photo_id, complaint_text))
            self.context.save_to_db()
        else:
            message = update.get_message()
            if message is not None:
                self.text = message.text

    async def send_message(self, update: Update):
        callback = update.get_callback_query()
        chat_id = update.get_chat_id()
        user = bot.DBController().get_user_by_chat_id(update.get_chat_id())
        other_user = bot.DBController().get_user_by_chat_id(self.other_chat_id)

        if self.share_contacts:
            self.share_contacts = False
            my_info, my_is_link = self.__generate_telegram_user_link(
                user.username, user.phone_number
            )
            text = "_С вами поделились контактами: {}_\n".format(
                user.profile_name
            )
            text += (
                "Ссылка на этого пользователя - {}\n".format(my_info)
                if my_is_link
                else "Номер этого пользователя - {}\n".format(my_info)
            )
            await update.bot.send_message(
                chat_id=self.other_chat_id, text=text, parse_mode="Markdown"
            )
            if callback is not None:
                await callback.answer()
            return

        if self.first_entered:
            kb = [
                [types.KeyboardButton(text="Выйти из чата")],
                [types.KeyboardButton(text="Поделиться контактами")],
                [types.KeyboardButton(text="Пожаловаться на собеседника")]
            ]
            keyboard = types.ReplyKeyboardMarkup(
                keyboard=kb, resize_keyboard=True, one_time_keyboard=True
            )
            await callback.message.answer(
                f"*Вы попали в анонимный чат с {other_user.profile_name}*",
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            await update.message_storage.open(chat_id, self.other_chat_id)
            delayed_messages = await update.message_storage.dump_messages(self.other_chat_id, chat_id)
            for message in delayed_messages:
                if isinstance(message, list):
                    if message[1] == "video_note":
                        video_note_id = message[0]
                        await callback.message.answer_video_note(video_note=video_note_id)
                    else:
                        voice_id = message[0]
                        await callback.message.answer_voice(voice=voice_id)
                else:
                    await callback.message.answer(message)
        else:
            is_closed = await update.message_storage.is_closed(self.other_chat_id, chat_id)
            if is_closed:
                await update.message_storage.put_message(chat_id, self.other_chat_id, self.text)
            else:
                if isinstance(self.text, list):
                    if self.text[1] == "video_note":
                        video_note_id = self.text[0]
                        await update.bot.send_video_note(chat_id=self.other_chat_id, video_note=video_note_id)
                    else:
                        voice_id = self.text[0]
                        await update.bot.send_voice(chat_id=self.other_chat_id, voice=voice_id)
                else:
                    await update.bot.send_message(chat_id=self.other_chat_id, text=self.text)

        if callback is not None:
            await callback.answer()

    @staticmethod
    def __generate_telegram_user_link(username, phone_number):
        if username:
            return f"https://t.me/{username}", True
        else:
            return phone_number, False

    async def get_complaint_text(self, update: Update):
        user = bot.DBController().get_user_by_chat_id(update.get_chat_id())
        other_user = bot.DBController().get_user_by_chat_id(self.other_chat_id)

        my_info, my_is_link = self.__generate_telegram_user_link(
            user.username, user.phone_number
        )
        other_info, other_is_link = self.__generate_telegram_user_link(
            other_user.username, other_user.phone_number
        )
        text = (f"  <b>От:</b> {user.profile_name} -- {my_info}\n"
                f"  <b>На:</b> {other_user.profile_name} -- {other_info}\n"
                f"\n")

        name = other_user.profile_name
        age = other_user.age
        city = other_user.city
        info = other_user.about
        id = other_user.chat_id
        preferences = tags.get_readable_tags_description(
            other_user.preferences_tags, self.context.bot_config
        )
        restrictions = tags.get_readable_tags_description(
            other_user.restrictions_tags, self.context.bot_config
        )
        diets = tags.get_readable_tags_description(
            other_user.dietary, self.context.bot_config
        )
        interests = tags.get_readable_tags_description(
            other_user.interests_tags, self.context.bot_config
        )
        photo_ids = other_user.photo_file_ids

        text += (f"<b>Анкета:</b>\n"
                 f"  <b>id:</b> {id}\n"
                 f"  <b>Имя:</b> {name}\n"
                 f"  <b>Возраст:</b> {age}\n"
                 f"  <b>Город:</b> {city}\n"
                 f"  <b>Пищевые предпочтения:</b> {preferences}\n"
                 f"  <b>Ограничения:</b> {restrictions}\n"
                 f"  <b>Диета:</b> {diets}\n"
                 f"  <b>Интересы:</b> {interests}\n"
                 f"  <b>О себе:</b> {info}")
        if photo_ids:
            return photo_ids[0], text
        else:
            return None, text
