from src.statemachine.State import State
import src.statemachine.state.photos as photos
import src.statemachine.state.photos.test as test
from src.bot.Update import Update
from aiogram import types

class PhotoUploadState(State):
    def __init__(self):
        super().__init__()
        self.text = "Загрузить фото..."

    def processUpdate(self, update: Update):
        message = update.getMessage()
        if message.photo:
            photo = message.photo[-1]
            photo_id = photo.file_id
            test.photo_ids.append(photo_id)
            self.nextState = photos.PhotosState()
            # save_to_db
        else:
            self.text = "Загрузите фото, а не файл."
            self.nextState = self

    def getNextState(self, update: Update):
        return self.nextState

    async def sendMessage(self, update: Update):
        message = update.getMessage()
        await message.answer(self.text)

