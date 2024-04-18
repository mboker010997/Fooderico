from src.statemachine import State
from src.statemachine.state import profile
from src.model import Update
from aiogram import types


class PhotoSelectionState(State):
    def __init__(self, context):
        super().__init__(context)
        self.is_error = False

    async def processUpdate(self, update: Update):
        if not update.getMessage():
            return
        message = update.getMessage()
        if (
            self.context.user.photo_file_ids is None
            or message.text != self.context.getMessage("photo_skipBtn")
        ):
            self.context.user.photo_file_ids = list()
            photo_ids = self.context.user.photo_file_ids
            if update.album is not None:
                obj = update.album[0]
                if obj.photo:
                    file_id = obj.photo[-1].file_id
                else:
                    file_id = obj[obj.content_type].file_id
                photo_ids.append(file_id)
            elif message.photo:
                photo = message.photo[-1]
                photo_id = photo.file_id
                photo_ids.append(photo_id)
            else:
                self.text = "Загрузите фото, а не файл/текст"
                self.is_error = True
                return
        self.context.setState(profile.AgeState(self.context))
        self.context.saveToDb()

    async def sendMessage(self, update: Update):
        if not update.getMessage():
            return
        message = update.getMessage()
        if self.is_error:
            await message.answer(self.text)
            return

        if self.context.user.photo_file_ids is not None:
            kb = [
                [
                    types.KeyboardButton(
                        text=self.context.getMessage("photo_skipBtn")
                    )
                ],
            ]
            keyboard = types.ReplyKeyboardMarkup(
                keyboard=kb, resize_keyboard=True, one_time_keyboard=True
            )
            await message.answer(
                self.context.getMessage("photo_text"), reply_markup=keyboard
            )
        else:
            await message.answer(
                self.context.getMessage("photo_text"),
                reply_markup=types.ReplyKeyboardRemove(),
            )
