from src.statemachine.State import State
import src.statemachine.state.menu as menu
import src.statemachine.state.photos as photos
import src.statemachine.state.photos.test as test
from src.bot.Update import Update
from aiogram import types


class PhotosState(State):
    def __init__(self):
        super().__init__()
        self.photo_listBtn = "Список фотографий"
        self.photo_uploadBtn = "Загрузить фото"
        self.menuBtn = "Вернуться в меню"
        self.nextStateDict = {
            self.photo_listBtn: photos.PhotoListState,
            self.photo_uploadBtn: photos.PhotoUploadState,
            self.menuBtn: menu.MenuState,
        }
    def processUpdate(self, update: Update):
        message = update.getMessage()
        if test.DELETE_PHOTO_COMMAND in message.text:
            photo_id = test.photo_ids[int(message.text[len(test.DELETE_PHOTO_COMMAND):])]
            test.photo_ids.remove(photo_id)

    def getNextState(self, update: Update):
        if update.getMessage().text in self.nextStateDict.keys():
            return self.nextStateDict[update.getMessage().text]()
        return self

    async def sendMessage(self, update: Update):
        message = update.getMessage()
        text = "Меню Фотоальбом"
        kb = [
            [types.KeyboardButton(text=self.photo_listBtn)],
            [types.KeyboardButton(text=self.photo_uploadBtn)],
            [types.KeyboardButton(text=self.menuBtn)],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
        await message.answer(text, reply_markup=keyboard)
