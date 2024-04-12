from src.statemachine import State
from src.statemachine.state import search, photos, profile, menu, chat
from src.model import Update
from aiogram import types
from src import bot


class MenuState(State):
    def __init__(self, context):
        super().__init__(context)
        self.searchBtn = "Поиск"
        self.photosBtn = "Фотоальбом"
        self.profileBtn = "Посмотреть профиль"
        self.statusBtn = "Статус пользователя"
        self.aboutBtn = "О сервисе"
        self.contactsBtn = "Последние действия"
        self.viewChatsBtn = context.getMessage("menu_view_chats")
        self.nextStateDict = {
            self.searchBtn: profile.GeoState,  # suggest changing geo before search
            self.photosBtn: photos.PhotosState,
            self.profileBtn: profile.ShowProfileState,
            self.statusBtn: menu.StatusState,
            self.viewChatsBtn: chat.ChatState,  # ChatListState
            self.aboutBtn: menu.AboutBotState,
            self.contactsBtn: search.ContactsState
        }

    def processUpdate(self, update: Update):
        if not update.getMessage():
            return
        message = update.getMessage()
        if message.text:
            if message.text in self.nextStateDict.keys():
                if message.text == self.searchBtn:
                    self.context.setNextState(search.SearchState)
                self.context.setState(self.nextStateDict.get(message.text)(self.context))
                self.context.saveToDb()

    async def sendMessage(self, update: Update):
        if not update.getMessage():
            return
        message = update.getMessage()
        text = "Главное меню"
        kb = [
            [types.KeyboardButton(text=self.searchBtn)],
            [types.KeyboardButton(text=self.photosBtn)],
            [types.KeyboardButton(text=self.profileBtn)],
            [types.KeyboardButton(text=self.statusBtn)],
            [types.KeyboardButton(text=self.viewChatsBtn)],
            [types.KeyboardButton(text=self.aboutBtn)],
            [types.KeyboardButton(text=self.contactsBtn)]
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb, resize_keyboard=True
        )
        return await message.answer(text, reply_markup=keyboard)
