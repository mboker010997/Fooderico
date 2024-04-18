from src.statemachine import State
from src.statemachine.state import search, photos, profile, menu, chat
from src.model import Update
from aiogram import types


class MenuState(State):
    def __init__(self, context):
        super().__init__(context)
        self.searchBtn = context.getMessage("menu_searchBtn")
        self.photosBtn = context.getMessage("menu_photosBtn")
        self.profileBtn = context.getMessage("menu_profileBtn")
        self.statusBtn = context.getMessage("menu_statusBtn")
        self.aboutBtn = context.getMessage("menu_aboutBtn")
        self.contactsBtn = context.getMessage("menu_recentActions")
        self.viewChatsBtn = context.getMessage("menu_view_chats")

        self.nextStateDict = {
            self.searchBtn: profile.GeoState,
            self.photosBtn: photos.PhotosState,
            self.profileBtn: profile.ShowProfileState,
            self.statusBtn: menu.StatusState,
            self.viewChatsBtn: chat.ChatListState,
            self.aboutBtn: menu.AboutBotState,
            self.contactsBtn: search.ContactsState,
        }

    async def processUpdate(self, update: Update):
        if not update.getMessage():
            return
        message = update.getMessage()
        if message.text:
            if message.text in self.nextStateDict.keys():
                if message.text == self.searchBtn:
                    self.context.setNextState(search.SearchState)
                self.context.setState(
                    self.nextStateDict.get(message.text)(self.context)
                )
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
            [types.KeyboardButton(text=self.contactsBtn)],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        return await message.answer(text, reply_markup=keyboard)
