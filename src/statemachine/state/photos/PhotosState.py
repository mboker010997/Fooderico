from src.statemachine.State import State
from src.statemachine.state import menu, photos
from src.model.Update import Update
from aiogram import types


class PhotosState(State):
    DELETE_PHOTO_COMMAND = "/delete_photo_"

    def __init__(self, context):
        super().__init__(context)
        self.photo_listBtn = self.context.getMessage("photo_listBtn")
        self.photo_uploadBtn = self.context.getMessage("photo_uploadBtn")
        self.menuBtn = self.context.getMessage("menuBtn")
        self.nextStateDict = {
            self.photo_listBtn: photos.PhotoListState,
            self.photo_uploadBtn: photos.PhotoUploadState,
            self.menuBtn: menu.MenuState,
        }

    def processUpdate(self, update: Update):
        if not update.getMessage():
            return
        message = update.getMessage()
        photo_ids = self.context.user.photo_file_ids
        if (message.text.startswith(PhotosState.DELETE_PHOTO_COMMAND)
                and message.text[len(PhotosState.DELETE_PHOTO_COMMAND):].isdigit()):
            photo_id = photo_ids[int(message.text[len(PhotosState.DELETE_PHOTO_COMMAND):])]
            photo_ids.remove(photo_id)
        if update.getMessage().text in self.nextStateDict.keys():
            self.context.setState(self.nextStateDict[update.getMessage().text](self.context))
        self.context.saveToDb()

    async def sendMessage(self, update: Update):
        chat_id = update.getChatId()
        text = self.context.getMessage("photos_text")
        kb = [
            [types.KeyboardButton(text=self.photo_listBtn)],
            [types.KeyboardButton(text=self.photo_uploadBtn)],
            [types.KeyboardButton(text=self.menuBtn)],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
        await update.bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
