from src.statemachine.State import State
from src.model.Update import Update
from aiogram import types
from src.statemachine.state import menu, profile


class ShowProfileState(State):
    def __init__(self, context):
        super().__init__(context)
        self.nextState = self

    def processUpdate(self, update: Update):
        if not update.getMessage():
            return
        answer = update.getMessage().text
        if answer == self.context.getMessage("edit_profileBtn"):
            self.context.setState(profile.UsernameState(self.context))
            self.context.saveToDb()
        elif answer == self.context.getMessage("menuBtn"):
            self.context.setState(menu.MenuState(self.context))
            self.context.saveToDb()

    async def sendMessage(self, update: Update):
        if not update.getMessage():
            return
        message = update.getMessage()
        text = self.context.getMessage("show_profile_text")
        await message.answer(text)
        kb = [
            [types.KeyboardButton(text=self.context.getMessage("edit_profileBtn"))],
            [types.KeyboardButton(text=self.context.getMessage("menuBtn"))],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
        photo_ids = self.context.user.photo_file_ids
        name = self.context.user.profile_name
        age = self.context.user.age
        city = self.context.user.city
        info = self.context.user.about

        func_tag_to_str = lambda x: self.context.getMessage(str(x))
        preferences = ', '.join(map(func_tag_to_str, self.context.user.preferences_tags))
        restrictions = ', '.join(map(func_tag_to_str, self.context.user.restrictions_tags))
        diets = ', '.join(map(func_tag_to_str, self.context.user.dietary))
        interests = ', '.join(map(func_tag_to_str, self.context.user.interests_tags))
        text = (self.context.getMessage("show_profile_template")
                .format(name, age, city, info, preferences, interests, diets, restrictions))
        if photo_ids:
            await message.answer_photo(photo=photo_ids[0], caption=text, reply_markup=keyboard)  # send only first photo
        else:
            await message.answer(text=text, reply_markup=keyboard)
