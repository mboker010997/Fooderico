from src.statemachine.State import State
from src.model.Update import Update
from aiogram import types
from src.statemachine.state import menu, profile


class ShowProfileState(State):
    def __init__(self, context):
        super().__init__(context)
        self.edit = "Редактировать"
        self.menu = "Вернуться в меню"
        self.nextState = self

    def processUpdate(self, update: Update):
        answer = update.getMessage().text
        if answer == self.edit:
            self.context.setState(profile.UsernameState(self.context))
            self.context.saveToDb()
        elif answer == self.menu:
            self.context.setState(menu.MenuState(self.context))
            self.context.saveToDb()

    async def sendMessage(self, update: Update):
        message = update.getMessage()
        text = "Ваш профиль:\n"
        await message.answer(text)
        kb = [
            [types.KeyboardButton(text=self.edit)],
            [types.KeyboardButton(text=self.menu)],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
        photo_ids = self.context.user.photo_file_ids
        name = self.context.user.profile_name
        age = self.context.user.age
        city = self.context.user.city
        info = self.context.user.about
        restrictions = ', '.join(map(str, self.context.user.restrictions_tags))
        interests = ', '.join(map(str, self.context.user.interests_tags))
        text = "{}, {}, {}\n{}\nИнтересы: {}\nОграничения: {}".format(name, age, city, info, interests, restrictions)
        if photo_ids:
            await message.answer_photo(photo=photo_ids[0], caption=text, reply_markup=keyboard)  # send only first photo
        else:
            await message.answer(text=text, reply_markup=keyboard)
