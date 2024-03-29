from src.statemachine.State import State
from src.statemachine.state.photos import PhotosState
from src import model


class PhotoListState(State):
    def __init__(self, context):
        super().__init__(context)

    def processUpdate(self, update: model.Update):
        print("in photo list")
        pass

    async def __switchContext(self, update: model.Update):
        self.context.setState(PhotosState(self.context))
        print("In context: ", self.context.state)
        print("In holder: ", model.StateUpdater.getState(update.getChatId()), update.getChatId())
        self.context.saveToDb()
        await self.context.state.sendMessage(update)

    async def sendMessage(self, update: model.Update):
        if not update.getMessage():
            return
        counter = 0
        message = update.getMessage()
        photo_ids = self.context.user.photo_file_ids
        if not photo_ids:
            await message.answer(self.context.getMessage("photo_list_empty"))
            await self.__switchContext(update)
            return
        for photo_id in photo_ids:
            await message.answer_photo(photo=photo_id, caption=PhotosState.DELETE_PHOTO_COMMAND+str(counter))
            counter += 1
        await self.__switchContext(update)
