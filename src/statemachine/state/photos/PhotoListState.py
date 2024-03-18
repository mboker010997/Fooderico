from src.statemachine.State import State
import src.statemachine.state.photos as photos
import src.statemachine.state.photos.test as test
from src.bot.Update import Update
from aiogram import types


class PhotoListState(State):
    def __init__(self):
        super().__init__()
        self.photo_list_empty = "Пусто"

    def processUpdate(self, update: Update):
        pass

    def getNextState(self, update: Update):
        return photos.PhotosState()

    async def sendMessage(self, update: Update):
        counter = 0
        message = update.getMessage()
        if not test.photo_ids:
            await message.answer(self.photo_list_empty)
            return
        for photo_id in test.photo_ids:
            await message.answer_photo(photo=photo_id)
            await message.answer(text=test.DELETE_PHOTO_COMMAND+str(counter))
            counter += 1
