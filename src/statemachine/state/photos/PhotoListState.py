from src.statemachine.State import State
# from src.statemachine.state.photos.PhotosState import PhotosState
from aiogram import types


class PhotoListState(State):
    def __init__(self, photo_file_ids):
        self.photo_file_ids = photo_file_ids

    def processUpdate(self, message: types.Message):
        pass

    def getNextState(self, message: types.Message):
        # return PhotosState(self.photo_file_ids)
        pass

    async def sendMessage(self, message: types.Message, bot, dp):
        if not self.photo_file_ids:
            await message.answer("Вы еще не загрузили ни одной фотографии")
            return
        await message.answer("Ваши фотографии:")
        for photo_file_id in self.photo_file_ids:
            await message.answer_photo(photo=photo_file_id)