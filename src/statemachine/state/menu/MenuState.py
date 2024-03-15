from src.statemachine.State import State
from src.statemachine.state.search.SearchState import SearchState
from src.statemachine.state.photos.PhotosState import PhotosState
from src.statemachine.state.profile.ShowProfileState import ShowProfileState
from src.statemachine.state.menu.StatusState import StatusState
import src.statemachine.state.menu as menu
from src.bot.Update import Update
from aiogram import types


class MenuState(State):
    def __init__(self):
        super().__init__()
        self.searchBtn = "Поиск"
        self.photosBtn = "Фотоальбом"
        self.profileBtn = "Посмотреть профиль"
        self.statusBtn = "Статус пользователя"
        self.aboutBtn = "О сервисе"
        self.nextStateDict = {
            self.searchBtn: SearchState(),
            self.photosBtn: PhotosState(),
            self.profileBtn: ShowProfileState(),
            self.statusBtn: StatusState(),
            self.aboutBtn: menu.AboutBotState(),
        }

    def processUpdate(self, update: Update):
        pass

    def getNextState(self, update: Update):
        return self.nextStateDict[update.getMessage().text]

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