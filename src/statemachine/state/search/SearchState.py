from src.statemachine import State
from src.statemachine.state import menu
from src.model import Update
from aiogram import types
from src.algo import similarity

class SearchState(State):
    def __init__(self, context):
        super().__init__(context)
        self.menu_text = "Главное меню"
        self.search_test = "Пользователь: "
        self.search_dislike = "Дизлайк"
        self.search_skip = "Пропустить"
        self.search_like = "Лайк"
        self.search_no_more_users = "Больше нет профилей"
        self.more = "Подробнее"
        self.view_photos = "Посмотреть фотоальбом"
        self.asked_view_photos = False
        self.asked_more = False
        self.nextStateDict = {
            self.menu_text: menu.MenuState,
        }

    def processUpdate(self, update: Update):
        # add relations to db: BLACKLIST, SKIPPED, FOLLOW
        message = update.getMessage()
        if message.text in self.nextStateDict.keys():
            self.context.setState(self.nextStateDict[update.getMessage().text](self.context))
            self.context.saveToDb()
            self.asked_more = False
            self.asked_view_photos = False
        elif message.text == self.more:
            self.asked_more = True
            self.asked_view_photos = False
        elif message.text == self.view_photos:
            self.asked_more = False
            self.asked_view_photos = True

    async def sendMessage(self, update: Update):
        # findUnknownUserBySimplePriority
        # user is found, if not found go to menu
        message = update.getMessage()
        other_user = self.context.user # todo: call sql_query to get right user FOOD-38
        photo_ids = other_user.photo_file_ids
        if self.asked_more:
            await self.__send_more_info(message, other_user, photo_ids)
        elif self.asked_view_photos:
            await self.__send_photos(message, photo_ids)
        else:
            await self.__send_user_info(message, other_user, photo_ids)

    async def __send_more_info(self, message, other_user, photo_ids):
        restrictions = ', '.join(map(str, other_user.restrictions_tags))
        interests = ', '.join(map(str, other_user.interests_tags))
        text = f"Ограничения: {restrictions}\nИнтересы: {interests}"
        keyboard = self.__create_keyboard(for_more=True, photos_exist=(len(photo_ids) > 0))
        await message.answer(text=text, reply_markup=keyboard)
        self.asked_more = False

    async def __send_photos(self, message, photo_ids):
        keyboard = self.__create_keyboard(for_photos=True, photos_exist=(len(photo_ids) > 0))
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
        return f"{name}, {age}, {city}\n{info}\nПроцент совпадения - {similarity_percentage}%"

    async def __send_user_info(self, message, other_user, photo_ids):
        text = self.__get_beautiful_info(other_user)
        keyboard = self.__create_keyboard(for_info=True, photos_exist = (len(photo_ids) > 0))
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
            kb.append([types.KeyboardButton(text=self.view_photos)])
        if for_photos:
            kb.append([types.KeyboardButton(text=self.more)])
        if for_info:
            kb.append([types.KeyboardButton(text=self.more)])
            if photos_exist:
                kb.append([types.KeyboardButton(text=self.view_photos)])
        return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
