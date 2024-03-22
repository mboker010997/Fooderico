from src.statemachine.State import State
from src.statemachine.state import photos
from src.model.Update import Update


class PhotoUploadState(State):
    def __init__(self, context):
        super().__init__(context)
        self.text = self.context.getMessage("photo_upload_text")

    def processUpdate(self, update: Update):
        message = update.getMessage()
        if self.context.user.photo_file_ids is None:
            self.context.user.photo_file_ids = list()
        photo_ids = self.context.user.photo_file_ids
        if message.photo:
            photo = message.photo[-1]
            photo_id = photo.file_id
            photo_ids.append(photo_id)
            self.context.setState(photos.PhotosState(self.context))
            self.context.saveToDb()
        else:
            self.text = self.context.getMessage("photo_upload_text")

    async def sendMessage(self, update: Update):
        message = update.getMessage()
        await message.answer(self.text)

