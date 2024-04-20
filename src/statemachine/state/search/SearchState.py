from src.statemachine import State
from src.statemachine.state import menu
from src.model.UserRelation import UserRelation
from src import bot
from src.model import Update, Tags as tags
from aiogram import types
from src.algo import similarity


class SearchState(State):
    def __init__(self, context):
        super().__init__(context)
        self.menu_text = self.context.get_message("menu_text")
        self.search_dislike = self.context.get_message("search_dislike")
        self.search_skip = self.context.get_message("search_skip")
        self.search_like = self.context.get_message("search_like")
        self.search_no_more_users = self.context.get_message("search_no_more_users")
        self.search_more = self.context.get_message("search_more")
        self.search_view_photos = self.context.get_message("search_view_photos")
        self.asked_view_photos = False
        self.asked_more = False
        self.last_relation = None
        self.is_match = False

        self.nextStateDict = {
            self.menu_text: menu.MenuState,
        }

    async def process_update(self, update: Update):
        # add relations to db: BLACKLIST, SKIPPED, FOLLOW
        if not update.get_message():
            return
        message = update.get_message()

        if message.text in self.nextStateDict.keys():
            self.context.set_state(self.nextStateDict[update.get_message().text](self.context))
            self.context.save_to_db()
            self.asked_more = False
            self.asked_view_photos = False
        elif message.text == self.search_more:
            self.asked_more = True
            self.asked_view_photos = False
        elif message.text == self.search_view_photos:
            self.asked_more = False
            self.asked_view_photos = True
        elif message.text in [
            self.search_like,
            self.search_dislike,
            self.search_skip,
        ]:
            self.last_relation.relation = message.text
            if self.last_relation.add_relation():
                self.is_match = True

    async def __notify_both(self, update: Update):
        my_user = bot.DBController().get_user(self.last_relation.user_id)
        other_user = bot.DBController().get_user(
            self.last_relation.other_user_id
        )

        await self.__send_match(update, my_user, other_user)
        await self.__send_match(update, other_user, my_user)
        self.is_match = False

    @staticmethod
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

    @staticmethod
    def __generate_telegram_user_link(username, phone_number):
        if username:
            return (f"https://t.me/{username}", True)
        else:
            return (phone_number, False)

    async def send_message(self, update: Update):
        if self.is_match:
            await self.__notify_both(update)
        message = update.get_message()
        chatId = update.get_chat_id()
        other_user = bot.MatchingClass().tags_matching_queue(chatId)
        if other_user is None:
            kb = [[types.KeyboardButton(text=self.menu_text)],
                  ]
            keyboard = types.ReplyKeyboardMarkup(
                keyboard=kb, resize_keyboard=True, one_time_keyboard=True
            )
            await message.answer(
                self.context.get_message("search_no_user_for_match"),
                reply_markup=keyboard,
            )
            return

        other_user = bot.DBController().get_user(other_user)

        photo_ids = other_user.photo_file_ids
        self.last_relation = UserRelation(
            self.context.user.id, other_user.id, None
        )
        if self.asked_more:
            await self.__send_more_info(message, other_user, photo_ids)
        elif self.asked_view_photos:
            await self.__send_photos(message, photo_ids)
        else:
            await self.__send_user_info(message, other_user, photo_ids)

    async def __send_more_info(self, message, other_user, photo_ids):
        preferences = tags.get_readable_tags_description(
            self.context.user.preferences_tags, self.context.bot_config
        )
        restrictions = tags.get_readable_tags_description(
            self.context.user.restrictions_tags, self.context.bot_config
        )
        diets = tags.get_readable_tags_description(
            self.context.user.dietary, self.context.bot_config
        )
        interests = tags.get_readable_tags_description(
            self.context.user.interests_tags, self.context.bot_config
        )

        text = (f"Пищевые предпочтения{preferences}\nОграничения: "
                f"{restrictions}\nДиета: {diets}\nИнтересы: {interests}")
        keyboard = self.__create_keyboard(
            for_more=True, photos_exist=(photo_ids and len(photo_ids) > 0)
        )
        await message.answer(text=text, reply_markup=keyboard)
        self.asked_more = False

    async def __send_photos(self, message, photo_ids):
        keyboard = self.__create_keyboard(
            for_photos=True, photos_exist=(photo_ids and len(photo_ids) > 0)
        )
        for photo_id in photo_ids:
            await message.answer_photo(photo=photo_id, reply_markup=keyboard)
        self.asked_view_photos = False

    def __get_beautiful_info(self, other_user):
        name = other_user.profile_name
        age = other_user.age
        city = other_user.city
        info = other_user.about
        similarity_percentage = similarity(
            self.context.user, other_user, self.context
        )
        return self.context.get_message("search_show_profile_template").format(
            name, age, city, info, similarity_percentage
        )

    async def __send_user_info(self, message, other_user, photo_ids):
        text = self.__get_beautiful_info(other_user)
        keyboard = self.__create_keyboard(
            for_info=True, photos_exist=(photo_ids and len(photo_ids) > 0)
        )
        if photo_ids:
            await message.answer_photo(
                photo=photo_ids[0], caption=text, reply_markup=keyboard
            )  # send only first photo
        else:
            await message.answer(text=text, reply_markup=keyboard)

    def __create_keyboard(self, for_more=False, for_photos=False, for_info=False, photos_exist=False):
        buttons = [
            [
                types.KeyboardButton(text=self.search_like),
                types.KeyboardButton(text=self.search_dislike),
            ],
            [
                types.KeyboardButton(text=self.search_skip)
            ],
        ]

        buttons_last_row = []
        if for_more and photos_exist:
            buttons_last_row.append(types.KeyboardButton(text=self.search_view_photos))
        if for_photos:
            buttons_last_row.append(types.KeyboardButton(text=self.search_more))
        if for_info:
            buttons_last_row.append(types.KeyboardButton(text=self.search_more))
            if photos_exist:
                buttons_last_row.append(types.KeyboardButton(text=self.search_view_photos))

        if buttons_last_row:
            buttons.append(buttons_last_row)

        buttons.append(
            [types.KeyboardButton(text=self.menu_text)],
        )

        return types.ReplyKeyboardMarkup(
            keyboard=buttons, resize_keyboard=True, one_time_keyboard=True
        )
