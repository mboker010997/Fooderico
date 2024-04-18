from src.statemachine.State import State
from src.statemachine.state.photos import PhotosState
from src import model
from aiogram import types


class PhotoListState(State):
    def __init__(self, context):
        super().__init__(context)

    async def process_update(self, update: model.Update):
        print("in photo list")
        pass

    async def __switchContext(self, update: model.Update):
        self.context.set_state(PhotosState(self.context))
        print("In context: ", self.context.state)
        print(
            "In holder: ",
            model.StateUpdater.getState(update.getChatId()),
            update.getChatId(),
        )
        self.context.save_to_db()
        await self.context.state.send_message(update)

    async def send_message(self, update: model.Update):
        if not update.getMessage():
            return
        counter = 0
        message = update.getMessage()
        photo_ids = self.context.user.photo_file_ids
        if not photo_ids:
            await message.answer(self.context.get_message("photo_list_empty"))
            await self.__switchContext(update)
            return
        for photo_id in photo_ids:
            if photo_id == photo_ids[0]:
                await message.answer_photo(photo=photo_id)
                counter += 1
                continue
            delete_button = types.InlineKeyboardButton(
                text="Удалить", callback_data=f"delete_photo_{counter}"
            )
            choose_main_button = types.InlineKeyboardButton(
                text="Выбрать главной",
                callback_data=f"choose_main_photo_{counter}",
            )
            keyboard = types.InlineKeyboardMarkup(
                inline_keyboard=[[choose_main_button, delete_button]]
            )
            await message.answer_photo(photo=photo_id, reply_markup=keyboard)
            counter += 1
        await self.__switchContext(update)
