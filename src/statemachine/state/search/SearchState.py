from src.statemachine.State import State
import src.statemachine.state.menu as menu
import src.statemachine.state.photos.test as test
from src.bot.Update import Update
from aiogram import types


class SearchState(State):
    def __init__(self):
        super().__init__()
        self.menu_text = "Главное меню"
        self.search_test = "Пользователь: "
        self.search_dislike = "Дизлайк"
        self.search_skip = "Пропустить"
        self.search_like = "Лайк"
        self.search_no_more_users = "Больше нет профилей"
        self.nextStateDict = {
            self.search_dislike: SearchState,
            self.search_skip: SearchState,
            self.search_like: SearchState,
            self.menu_text: menu.MenuState,
        }

    def processUpdate(self, update: Update):
        #add relations to db: BLACKLIST, SKIPPED, FOLLOW
        pass

    def getNextState(self, update: Update):
        if update.getMessage().text in self.nextStateDict.keys():
            return self.nextStateDict[update.getMessage().text]()
        return self

    async def sendMessage(self, update: Update):
        # findUnknownUserBySimplePriority
        # user is found, if not found go to menu
        message = update.getMessage()
        for photo_id in test.photo_ids:
            await message.answer_photo(photo=photo_id)
        kb = [
            [types.KeyboardButton(text=self.search_dislike)],
            [types.KeyboardButton(text=self.search_skip)],
            [types.KeyboardButton(text=self.search_like)],
            [types.KeyboardButton(text=self.menu_text)],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
        await message.answer(self.search_test, reply_markup=keyboard)
