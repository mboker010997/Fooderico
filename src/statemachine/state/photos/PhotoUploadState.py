from src.statemachine.State import State
import src.statemachine.state.photos as photos
import src.statemachine.state.photos.test as test
from src.bot.Update import Update
from aiogram import types

class PhotoUploadState(State):
    def __init__(self):
        super().__init__()

    def processUpdate(self, update: Update):
        message = update.getMessage()
        if message.photo:
            photo = message.photo[-1]
            photo_file_id = photo.file_id
            test.photo_ids.append(photo_file_id)
            # save_to_db

    def getNextState(self, update: Update):
        return photos.PhotosState()
        pass

    async def sendMessage(self, update: Update):
        text = "Загрузить фото..."
        message = update.getMessage()
        await message.answer(text)

