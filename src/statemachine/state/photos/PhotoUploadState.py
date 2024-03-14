from src.statemachine.State import State
# from src.statemachine.state.photos.PhotosState import PhotosState
from aiogram import types

class PhotoUploadState(State):
    def __init__(self):
        super().__init__()
        self.photo_file_ids = []

    def processUpdate(self, message: types.Message):
        if message.photo:
            photo = message.photo[-1]
            photo_file_id = photo.file_id
            self.photo_file_ids.append(photo_file_id)
            # save_to_db

    def getNextState(self, message: types.Message):
        # return PhotosState(self.photo_file_ids)
        pass

    async def sendMessage(self, message: types.Message, bot, dp):
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(text="Загрузить фото")]],
            one_time_keyboard=True
        )
        await message.answer("Загрузите фотографии", reply_markup=keyboard)

