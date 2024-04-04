from src.statemachine import State
from src.statemachine.state import profile
from src.model.Update import Update
from src.model import Tags as tags
from aiogram import types


class RestrictionsTagState(State):
    def __init__(self, context):
        super().__init__(context)
        self.options = tags.restrictionsTags
        self.hasPoll = True

    def processUpdate(self, update: Update):
        message = update.getMessage()

        if self.context.user.restrictions_tags is not None and message is not None and message.text == self.context.getMessage("restrictions_skipBtn"):
            self.context.setState(profile.DietsTagState(self.context))
            self.context.saveToDb()
            self.hasPoll = False
            return

        poll_answer = update.getPollAnswer()
        if poll_answer and int(poll_answer.poll_id) == int(self.context.user.active_poll_id):
            self.context.user.restrictions_tags = set()
            for option_id in poll_answer.option_ids:
                self.context.user.restrictions_tags.add(self.options[option_id])
            self.context.user.active_poll_id = update.getPollAnswer().poll_id
            self.context.setState(profile.DietsTagState(self.context))
            self.context.saveToDb()
        self.hasPoll = False

    async def sendMessage(self, update: Update):
        options = list(map(lambda x: self.context.getMessage(x), tags.restrictionsTags))

        kb = [
            [types.KeyboardButton(text=self.context.getMessage("restrictions_skipBtn"))],
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb, resize_keyboard=True, one_time_keyboard=True
        )

        if self.hasPoll:
            if self.context.user.restrictions_tags is not None:
                poll_info = await update.bot.send_poll(chat_id=update.getChatId(),
                                                       question=self.context.getMessage("restrictions_tag_text"),
                                                       options=options,
                                                       is_anonymous=False,
                                                       allows_multiple_answers=True,
                                                       reply_markup=keyboard)
            else:
                poll_info = await update.bot.send_poll(chat_id=update.getChatId(),
                                                       question=self.context.getMessage("restrictions_tag_text"),
                                                       options=options,
                                                       is_anonymous=False,
                                                       allows_multiple_answers=True,
                                                       reply_markup=types.ReplyKeyboardRemove())
        self.context.user.active_poll_id = poll_info.poll.id
        self.context.saveToDb()
