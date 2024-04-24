from src.statemachine.State import State
from src.statemachine.state.photos import PhotosState
from src.model.Update import Update
from aiogram import types


class PhotoListState(State):
    def __init__(self, context):
        super().__init__(context)

    async def process_update(self, update: Update):
        pass

    async def __switch_context(self, update: Update):
        self.context.set_state(PhotosState(self.context))
        self.context.save_to_db()
        await self.context.state.send_message(update)

    async def send_message(self, update: Update):
        if not update.get_message():
            return

        message = update.get_message()
        photo_ids = self.context.user.photo_file_ids

        if not photo_ids:
            await message.answer(self.context.get_message("photo_list_empty"))
            await self.__switch_context(update)
            return

        counter = 0
        for photo_id in photo_ids:
            if photo_id == photo_ids[0]:
                await message.answer_photo(photo=photo_id)
                counter += 1
                continue

            choose_button = types.InlineKeyboardButton(
                text=self.context.get_message("photo_choose"), callback_data=f"choose_main_photo_{counter}"
            )
            del_button = types.InlineKeyboardButton(
                text=self.context.get_message("photo_delete"), callback_data=f"delete_photo_{counter}"
            )

            keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[choose_button, del_button]])
            await message.answer_photo(photo=photo_id, reply_markup=keyboard)
            counter += 1

        await self.__switch_context(update)
