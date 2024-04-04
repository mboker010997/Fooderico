from src.statemachine import State
from src.statemachine.state import menu
from src.model.UserRelation import UserRelation
from src import bot
from src.model import Update
from aiogram import types
from src.algo import similarity


class SearchState(State):
    def __init__(self, context):
        super().__init__(context)
        self.menu_text = self.context.getMessage("menu_text")
        self.search_dislike = self.context.getMessage("search_dislike")
        self.search_skip = self.context.getMessage("search_skip")
        self.search_like = self.context.getMessage("search_like")
        self.search_no_more_users = self.context.getMessage("search_no_more_users")
        self.search_more = self.context.getMessage("search_more")
        self.search_view_photos = self.context.getMessage("search_view_photos")
        self.asked_view_photos = False
        self.asked_more = False
        self.last_relation = None
        self.is_match = False
        self.nextStateDict = {
            self.menu_text: menu.MenuState,
        }

    def processUpdate(self, update: Update):
        # add relations to db: BLACKLIST, SKIPPED, FOLLOW
        if not update.getMessage():
            return
        message = update.getMessage()
        if message.text in self.nextStateDict.keys():
            self.context.setState(self.nextStateDict[update.getMessage().text](self.context))
            self.context.saveToDb()
            self.asked_more = False
            self.asked_view_photos = False
        elif message.text == self.search_more:
            self.asked_more = True
            self.asked_view_photos = False
        elif message.text == self.search_view_photos:
            self.asked_more = False
            self.asked_view_photos = True
        elif message.text in [self.search_like, self.search_dislike, self.search_skip]:
            self.last_relation.relation = message.text
            if self.last_relation.add_relation():
                self.is_match = True

    async def __notify_both(self, update: Update):
        my_chat_id = bot.DBController().getUser(self.last_relation.user_id).chat_id
        my_profile_name = bot.DBController().getUser(self.last_relation.user_id).profile_name
        other_chat_id = bot.DBController().getUser(self.last_relation.other_user_id).chat_id
        other_profile_name = bot.DBController().getUser(self.last_relation.other_user_id).profile_name
        await update.bot.send_message(chat_id=my_chat_id, text="Вас лайкнул в ответ {}".format(other_profile_name))
        await update.bot.send_message(chat_id=other_chat_id, text="Вас лайкнул в ответ {}".format(my_profile_name))
        self.is_match = False

    async def sendMessage(self, update: Update):
        message = update.getMessage()
        chatId = update.getChatId()
        # todo (Bakyt): (FOOD-10) - Uncomment this:
        # other_user = bot.DBController().KirillsTagsMatchingUser(chatId) # rename if it is necessary
        # if other_user is None:
        #     kb = [
        #         [types.KeyboardButton(text=self.menu_text)],
        #     ]
        #     keyboard = types.ReplyKeyboardMarkup(
        #         keyboard=kb, resize_keyboard=True, one_time_keyboard=True
        #     )
        #     await message.answer(self.context.getMessage("search_no_user_for_match"), reply_markup=keyboard)
        #     return
        # other_user = bot.DBController().getUser(other_user)

        # todo (Bakyt): (FOOD-10) - Delete this:
        other_users = bot.DBController().tagsMatchingQueue(chatId)
        if other_users:
            other_user = other_users[0]
            other_user = bot.DBController().getUser(other_user)
        else:
            kb = [
                [types.KeyboardButton(text=self.menu_text)],
            ]
            keyboard = types.ReplyKeyboardMarkup(
                keyboard=kb, resize_keyboard=True, one_time_keyboard=True
            )
            await message.answer(self.context.getMessage("search_no_user_for_match"), reply_markup=keyboard)
            return
        #

        photo_ids = other_user.photo_file_ids
        self.last_relation = UserRelation(self.context.user.id, other_user.id, None)
        if self.asked_more:
            await self.__send_more_info(message, other_user, photo_ids)
        elif self.asked_view_photos:
            await self.__send_photos(message, photo_ids)
        else:
            await self.__send_user_info(message, other_user, photo_ids)
        if self.is_match:
            await self.__notify_both(update)

    async def __send_more_info(self, message, other_user, photo_ids):
        func_tag_to_str = lambda x: self.context.getMessage(str(x))
        preferences = ', '.join(map(func_tag_to_str, other_user.preferences_tags))
        restrictions = ', '.join(map(func_tag_to_str, other_user.restrictions_tags))
        diets = ', '.join(map(func_tag_to_str, other_user.dietary))
        interests = ', '.join(map(func_tag_to_str, other_user.interests_tags))

        text = f"Пищевые предпочтения{preferences}\nОграничения: {restrictions}\nДиета: {diets}\nИнтересы: {interests}"
        keyboard = self.__create_keyboard(for_more=True, photos_exist=(photo_ids and len(photo_ids) > 0))
        await message.answer(text=text, reply_markup=keyboard)
        self.asked_more = False

    async def __send_photos(self, message, photo_ids):
        keyboard = self.__create_keyboard(for_photos=True, photos_exist=(photo_ids and len(photo_ids) > 0))
        for photo_id in photo_ids:
            await message.answer_photo(photo=photo_id, reply_markup=keyboard)
        self.asked_view_photos = False

    def __get_beautiful_info(self, other_user):
        name = other_user.profile_name
        age = other_user.age
        city = other_user.city
        info = other_user.about
        other_tags = other_user.restrictions_tags.union(other_user.interests_tags)
        my_tags = self.context.user.interests_tags.union(self.context.user.restrictions_tags)
        similarity_percentage = similarity(other_tags, my_tags)
        return (self.context.getMessage("search_show_profile_template")
                .format(name, age, city, info, similarity_percentage))

    async def __send_user_info(self, message, other_user, photo_ids):
        text = self.__get_beautiful_info(other_user)
        keyboard = self.__create_keyboard(for_info=True, photos_exist = (photo_ids and len(photo_ids) > 0))
        if photo_ids:
            await message.answer_photo(photo=photo_ids[0], caption=text, reply_markup=keyboard)  # send only first photo
        else:
            await message.answer(text=text, reply_markup=keyboard)

    def __create_keyboard(self, for_more=False, for_photos=False, for_info=False, photos_exist=False):
        kb = [
            [types.KeyboardButton(text=self.search_dislike)],
            [types.KeyboardButton(text=self.search_skip)],
            [types.KeyboardButton(text=self.search_like)],
            [types.KeyboardButton(text=self.menu_text)],
        ]
        if for_more and photos_exist:
            kb.append([types.KeyboardButton(text=self.search_view_photos)])
        if for_photos:
            kb.append([types.KeyboardButton(text=self.search_more)])
        if for_info:
            kb.append([types.KeyboardButton(text=self.search_more)])
            if photos_exist:
                kb.append([types.KeyboardButton(text=self.search_view_photos)])
        return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
