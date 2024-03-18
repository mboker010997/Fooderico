from src.statemachine import State
from src.statemachine.state import menu
from src.model import Update
from aiogram import types


class SearchState(State):
    def __init__(self, context):
        super().__init__(context)
        self.menu_text = "Главное меню"
        self.search_test = "Пользователь: "
        self.search_dislike = "Дизлайк"
        self.search_skip = "Пропустить"
        self.search_like = "Лайк"
        self.search_no_more_users = "Больше нет профилей"
        self.nextStateDict = {
            self.menu_text: menu.MenuState,
        }

    def processUpdate(self, update: Update):
        # add relations to db: BLACKLIST, SKIPPED, FOLLOW
        if update.getMessage().text in self.nextStateDict.keys():
            self.context.setState(self.nextStateDict[update.getMessage().text](self.context))
            self.context.saveToDb()

    async def sendMessage(self, update: Update):
        # findUnknownUserBySimplePriority
        # user is found, if not found go to menu
        message = update.getMessage()
        photo_ids = self.context.user.photo_file_ids
        for photo_id in photo_ids:
            await message.answer_photo(photo=photo_id)
        kb = [
            [types.KeyboardButton(text=self.search_dislike)],
            [types.KeyboardButton(text=self.search_skip)],
            [types.KeyboardButton(text=self.search_like)],
            [types.KeyboardButton(text=self.menu_text)],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
        await message.answer(self.search_test, reply_markup=keyboard)
