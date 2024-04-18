from src.statemachine.State import State
from src.statemachine.state import photos
from src.model.Update import Update
from aiogram import types


class PhotoUploadState(State):
    def __init__(self, context):
        super().__init__(context)
        self.text = self.context.get_message("photo_upload_text")
        self.exit_command = "/exit"
        self.is_error = False

    async def process_update(self, update: Update):
        if not update.getMessage():
            return
        message = update.getMessage()
        if self.context.user.photo_file_ids is None:
            self.context.user.photo_file_ids = list()
        photo_ids = self.context.user.photo_file_ids
        if self.is_error and message.text == "Назад":
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
        if not update.getMessage():
            return
        message = update.getMessage()
        kb = [
            [types.KeyboardButton(text="Назад")],
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb, resize_keyboard=True, one_time_keyboard=True
        )
        if self.is_error:
            await message.answer(self.text, reply_markup=keyboard)
        else:
            await message.answer(self.text)
