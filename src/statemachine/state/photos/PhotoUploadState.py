from src.statemachine.State import State
from src.statemachine.state import photos
from src.model.Update import Update
from aiogram import types


class PhotoUploadState(State):
    def __init__(self, context):
        super().__init__(context)
        self.text = self.context.get_message("photo_upload_text")
        self.is_error = False

    async def process_update(self, update: Update):
        if not update.get_message():
            return

        if self.context.user.photo_file_ids is None:
            self.context.user.photo_file_ids = list()
        photo_ids = self.context.user.photo_file_ids

        message = update.get_message()
        if self.is_error and message.text == self.context.get_message("photo_back"):
            self.is_error = False
            self.context.set_state(photos.PhotosState(self.context))
            self.context.save_to_db()

        if update.album is not None:
            for obj in update.album:
                if obj.photo:
                    file_id = obj.photo[-1].file_id
                else:
                    file_id = obj[obj.content_type].file_id
                photo_ids.append(file_id)
            self.context.set_state(photos.PhotosState(self.context))
            self.context.save_to_db()
        elif message.photo:
            photo = message.photo[-1]
            photo_id = photo.file_id
            photo_ids.append(photo_id)
            self.context.set_state(photos.PhotosState(self.context))
            self.context.save_to_db()
        else:
            self.text = self.context.get_message("photo_upload_error")
            self.is_error = True

    async def send_message(self, update: Update):
        if not update.get_message():
            return

        buttons = [
            [types.KeyboardButton(text=self.context.get_message("photo_back"))],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)

        message = update.get_message()
        if self.is_error:
            await message.answer(self.text, reply_markup=keyboard)
        else:
            await message.answer(self.text)
