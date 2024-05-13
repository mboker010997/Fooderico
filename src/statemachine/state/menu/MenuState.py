from src.statemachine import State
from src.statemachine.state import search, photos, profile, menu, chat, constructor, admin
from src.model import Update
from aiogram import types
from src import bot


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
        self.constructorMenuBtn = context.get_message("menu_constructor_menu")
        self.feedback = context.get_message("menu_feedback")
        self.adminBtn = context.get_message("menu_adminBtn")

        self.nextStateDict = {
            self.searchBtn: profile.GeoState,
            self.photosBtn: photos.PhotosState,
            self.profileBtn: profile.ShowProfileState,
            self.statusBtn: menu.StatusState,
            self.viewChatsBtn: chat.ChatListState,
            self.aboutBtn: menu.AboutBotState,
            self.contactsBtn: search.ContactsState,
            self.constructorMenuBtn: constructor.ConstructorMenuState,
            self.feedback: menu.FeedbackState,
            self.adminBtn: admin.AdminState,
        }

    async def process_update(self, update: Update):
        if not update.get_message():
            return
        text = update.get_message().text
        if text:
            if text in self.nextStateDict.keys():
                if text == self.searchBtn:
                    self.context.set_next_state(search.SearchState)
                print(str(update.get_chat_id()), bot.DBController().get_all_admins())
                if text == self.adminBtn and str(update.get_chat_id()) not in bot.DBController().get_all_admins():
                    return
                self.context.set_state(self.nextStateDict.get(text)(self.context))
                self.context.save_to_db()

    async def send_message(self, update: Update):
        if not update.get_message():
            return
        message = update.get_message()
        text = "Главное меню"
        buttons = [
            [types.KeyboardButton(text=self.searchBtn), types.KeyboardButton(text=self.constructorMenuBtn)],
            [types.KeyboardButton(text=self.photosBtn), types.KeyboardButton(text=self.profileBtn)],
            [types.KeyboardButton(text=self.statusBtn), types.KeyboardButton(text=self.viewChatsBtn)],
            [types.KeyboardButton(text=self.contactsBtn), types.KeyboardButton(text=self.feedback),
             types.KeyboardButton(text=self.aboutBtn)],
        ]
        if str(update.get_chat_id()) in bot.DBController().get_all_admins():
            buttons.append([types.KeyboardButton(text=self.adminBtn)])
        keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
        return await message.answer(text, reply_markup=keyboard)
