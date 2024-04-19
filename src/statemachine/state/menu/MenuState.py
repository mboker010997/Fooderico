from src.statemachine import State
from src.statemachine.state import search, photos, profile, menu, chat
from src.model import Update
from aiogram import types


class MenuState(State):
    def __init__(self, context):
        super().__init__(context)
        self.searchBtn = context.get_message("menu_searchBtn")
        self.photosBtn = context.get_message("menu_photosBtn")
        self.profileBtn = context.get_message("menu_profileBtn")
        self.statusBtn = context.get_message("menu_statusBtn")
        self.aboutBtn = context.get_message("menu_aboutBtn")
        self.contactsBtn = context.get_message("menu_recentActions")
        self.viewChatsBtn = context.get_message("menu_view_chats")

        self.nextStateDict = {
            self.searchBtn: profile.GeoState,
            self.photosBtn: photos.PhotosState,
            self.profileBtn: profile.ShowProfileState,
            self.statusBtn: menu.StatusState,
            self.viewChatsBtn: chat.ChatListState,
            self.aboutBtn: menu.AboutBotState,
            self.contactsBtn: search.ContactsState,
        }

    async def process_update(self, update: Update):
        if not update.getMessage():
            return
        message = update.getMessage()
        if message.text:
            if message.text in self.nextStateDict.keys():
                if message.text == self.searchBtn:
                    self.context.set_next_state(search.SearchState)
                self.context.set_state(self.nextStateDict.get(message.text)(self.context))
                self.context.save_to_db()

    async def send_message(self, update: Update):
        if not update.getMessage():
            return
        message = update.getMessage()
        text = "Главное меню"
        buttons = [
            [types.KeyboardButton(text=self.searchBtn)],
            [types.KeyboardButton(text=self.photosBtn), types.KeyboardButton(text=self.profileBtn)],
            [types.KeyboardButton(text=self.statusBtn), types.KeyboardButton(text=self.viewChatsBtn)],
            [types.KeyboardButton(text=self.contactsBtn), types.KeyboardButton(text=self.aboutBtn)],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
        return await message.answer(text, reply_markup=keyboard)
