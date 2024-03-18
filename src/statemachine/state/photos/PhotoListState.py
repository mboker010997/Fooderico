from src.statemachine.State import State
from src.statemachine.state.photos import PhotosState
from src.model import Update


class PhotoListState(State):
    def __init__(self, context):
        super().__init__(context)
        self.PHOTO_LIST_EMPTY = "Пусто"

    def processUpdate(self, update: Update):
        pass

    async def __switchContext(self, update: Update):
        self.context.setState(PhotosState(self.context))
        self.context.saveToDb()
        await self.context.state.sendMessage(update)

    async def sendMessage(self, update: Update):
        counter = 0
        message = update.getMessage()
        photo_ids = self.context.user.photo_file_ids
        if not photo_ids:
            await message.answer(self.PHOTO_LIST_EMPTY)
            await self.__switchContext(update)
            return
        for photo_id in photo_ids:
            await message.answer_photo(photo=photo_id, caption=PhotosState.DELETE_PHOTO_COMMAND+str(counter))
            counter += 1
        await self.__switchContext(update)
