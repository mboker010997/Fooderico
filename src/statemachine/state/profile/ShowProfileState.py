from src.statemachine.State import State
from src.model.Update import Update
from aiogram import types
from src.statemachine.state import menu, profile
from src.model import Tags as TagsModel


class ShowProfileState(State):
    def __init__(self, context):
        super().__init__(context)
        self.nextState = self

    async def process_update(self, update: Update):
        if not update.get_message():
            return
        answer = update.get_message().text
        if answer == self.context.get_message("edit_profileBtn"):
            self.context.set_state(profile.UsernameState(self.context))
            self.context.save_to_db()
        elif answer == self.context.get_message("menuBtn"):
            self.context.set_state(menu.MenuState(self.context))
            self.context.save_to_db()

    async def send_message(self, update: Update):
        if not update.get_message():
            return
        message = update.get_message()
        text = self.context.get_message("show_profile_text")
        await message.answer(text)
        buttons = [
            [types.KeyboardButton(text=self.context.get_message("edit_profileBtn"))],
            [types.KeyboardButton(text=self.context.get_message("menuBtn"))],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
        photo_ids = self.context.user.photo_file_ids
        name = self.context.user.profile_name
        age = self.context.user.age
        city = self.context.user.city
        info = self.context.user.about

        preferences = TagsModel.get_readable_tags_description(
            self.context.user.preferences_tags, self.context.bot_config
        )
        restrictions = TagsModel.get_readable_tags_description(
            self.context.user.restrictions_tags, self.context.bot_config
        )
        diets = TagsModel.get_readable_tags_description(self.context.user.dietary, self.context.bot_config)
        interests = TagsModel.get_readable_tags_description(self.context.user.interests_tags, self.context.bot_config)

        text = self.context.get_message("show_profile_template").format(
            name, age, city, info, preferences, restrictions, diets, interests
        )
        if photo_ids:
            await message.answer_photo(
                photo=photo_ids[0], caption=text, reply_markup=keyboard
            )  # send only first photo
        else:
            await message.answer(text=text, reply_markup=keyboard)
