from src.statemachine import State
from src.statemachine.state import search, photos, profile, menu
from src.model import Update
from aiogram import types


class MenuState(State):
    def __init__(self, context):
        super().__init__(context)
        self.searchBtn = "Поиск"
        self.photosBtn = "Фотоальбом"
        self.profileBtn = "Посмотреть профиль"
        self.statusBtn = "Статус пользователя"
        self.aboutBtn = "О сервисе"
        self.nextStateDict = {
            self.searchBtn: search.SearchState,
            self.photosBtn: photos.PhotosState,
            self.profileBtn: profile.ShowProfileState,
            self.statusBtn: menu.StatusState,
            self.aboutBtn: menu.AboutBotState,
        }

    def processUpdate(self, update: Update):
        text = update.getMessage().text
        if text in self.nextStateDict.keys():
            self.context.setState(self.nextStateDict.get(text)(self.context))
            self.context.saveToDb()

    async def sendMessage(self, update: Update):
        message = update.getMessage()
        text = "Главное меню"
        kb = [
            [types.KeyboardButton(text=self.searchBtn)],
            [types.KeyboardButton(text=self.photosBtn)],
            [types.KeyboardButton(text=self.profileBtn)],
            [types.KeyboardButton(text=self.statusBtn)],
            [types.KeyboardButton(text=self.aboutBtn)],
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb, resize_keyboard=True, one_time_keyboard=True
        )
        await message.answer(text, reply_markup=keyboard)