from src.statemachine.State import State
from src.statemachine.state import menu, photos
from src.model.Update import Update
from aiogram import types


class PhotosState(State):
    def __init__(self, context):
        super().__init__(context)
        self.photo_list_btn = self.context.get_message("photo_listBtn")
        self.photo_upload_btn = self.context.get_message("photo_uploadBtn")
        self.menu_btn = self.context.get_message("menuBtn")
        self.next_state_dict = {
            self.photo_list_btn: photos.PhotoListState,
            self.photo_upload_btn: photos.PhotoUploadState,
            self.menu_btn: menu.MenuState,
        }

    async def process_update(self, update: Update):
        if not update.get_message():
            return

        message = update.get_message()
        if message.text and message.text in self.next_state_dict.keys():
            self.context.set_state(self.next_state_dict[update.get_message().text](self.context))
        self.context.save_to_db()

    async def send_message(self, update: Update):
        chat_id = update.get_chat_id()
        text = self.context.get_message("photos_text")
        buttons = [
            [types.KeyboardButton(text=self.photo_list_btn)],
            [types.KeyboardButton(text=self.photo_upload_btn)],
            [types.KeyboardButton(text=self.menu_btn)],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
        message = await update.bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
        return message
