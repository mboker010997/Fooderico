from src.statemachine import State
from src.model import Update
from src.statemachine.state import profile
from aiogram import types
from src.bot import Matching


class AboutState(State):
    def __init__(self, context):
        super().__init__(context)

    async def processUpdate(self, update: Update):
        if not update.getMessage():
            return
        message = update.getMessage()

        if (
            self.context.user.about is None
            or message.text != self.context.getMessage("about_skipBtn")
        ):
            self.context.user.about = message.text
            self.context.user.others_interests = (
                Matching.MatchingClass().getOtherTags(message.text)
            )

        self.context.setState(profile.OtherInterests(self.context))
        self.context.saveToDb()

    async def sendMessage(self, update: Update):
        if not update.getMessage():
            return
        message = update.getMessage()

        if self.context.user.about is not None:
            kb = [
                [
                    types.KeyboardButton(
                        text=self.context.getMessage("about_skipBtn")
                    )
                ],
            ]
            keyboard = types.ReplyKeyboardMarkup(
                keyboard=kb, resize_keyboard=True, one_time_keyboard=True
            )
            await message.answer(
                self.context.getMessage("about_text"), reply_markup=keyboard
            )
        else:
            await message.answer(
                self.context.getMessage("about_text"),
                reply_markup=types.ReplyKeyboardRemove(),
            )
