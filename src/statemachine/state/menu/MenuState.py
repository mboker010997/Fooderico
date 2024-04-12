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
            self.viewChatsBtn: chat.ChatListState,
            self.aboutBtn: menu.AboutBotState,
            self.contactsBtn: search.ContactsState
        }
        self.CHANGE_TO_LIKE_COMMAND = "/change_to_like_"
        self.CHANGE_TO_DISLIKE_COMMAND = "/change_to_dislike_"
        self.CHANGE_TO_SKIP_COMMAND = "/change_to_skip_"
        self.REMOVE_RELATION_COMMAND = "/remove_"

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
            elif message.text.startswith(
                    (self.CHANGE_TO_LIKE_COMMAND, self.CHANGE_TO_DISLIKE_COMMAND, self.CHANGE_TO_SKIP_COMMAND, self.REMOVE_RELATION_COMMAND)):
                query = (f"SELECT * FROM tele_meet_relations WHERE user_id = {self.context.user.id}")
                bot.DBController().cursor.execute(query)
                self.other_user_rows = bot.DBController().cursor.fetchall()
                command, num = None, None

                if message.text.startswith(self.CHANGE_TO_LIKE_COMMAND):
                    command = 'FOLLOW'
                    num = int(message.text[len(self.CHANGE_TO_LIKE_COMMAND):])
                elif message.text.startswith(self.CHANGE_TO_DISLIKE_COMMAND):
                    command = 'BLACKLIST'
                    num = int(message.text[len(self.CHANGE_TO_DISLIKE_COMMAND):])
                elif message.text.startswith(self.CHANGE_TO_SKIP_COMMAND):
                    command = 'SKIPPED'
                    num = int(message.text[len(self.CHANGE_TO_SKIP_COMMAND):])
                elif message.text.startswith(self.REMOVE_RELATION_COMMAND):
                    num = int(message.text[len(self.REMOVE_RELATION_COMMAND):])
                if num is not None and 0 <= num < len(self.other_user_rows):
                    other_user_id = self.other_user_rows[num][2]
                    if command:
                        bot.DBController().cursor.execute(
                            f"UPDATE tele_meet_relations SET relation = '{command}' WHERE user_id = {self.context.user.id} AND other_user_id = {other_user_id};")
                    else:
                        bot.DBController().cursor.execute(
                            f"DELETE FROM tele_meet_relations WHERE user_id = {self.context.user.id} AND other_user_id = {other_user_id};")

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
