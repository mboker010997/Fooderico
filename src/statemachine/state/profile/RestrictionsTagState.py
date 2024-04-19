from src.statemachine import State
from src.statemachine.state import profile
from src.model.Update import Update
from src.model import Tags as TagsModel
from aiogram import types


class RestrictionsTagState(State):
    def __init__(self, context):
        super().__init__(context)
        self.options = TagsModel.restrictionsTags.copy()
        self.options.append(TagsModel.nothing_tag)
        self.hasPoll = True

    async def process_update(self, update: Update):
        message = update.getMessage()

        if (
            self.context.user.restrictions_tags is not None
            and message is not None
            and message.text == self.context.get_message("restrictions_skipBtn")
        ):
            self.context.set_state(profile.DietsTagState(self.context))
            self.context.save_to_db()
            self.hasPoll = False
            return

        poll_answer = update.getPollAnswer()
        if poll_answer and int(poll_answer.poll_id) == int(self.context.user.active_poll_id):
            self.context.user.restrictions_tags = set()
            for option_id in poll_answer.option_ids:
                option_name = self.options[option_id]
                if option_name == TagsModel.nothing_tag:
                    continue
                self.context.user.restrictions_tags.add(option_name)
            self.context.user.active_poll_id = update.getPollAnswer().poll_id
            self.context.set_state(profile.DietsTagState(self.context))
            self.context.save_to_db()
        self.hasPoll = False

    async def send_message(self, update: Update):
        options = list(map(lambda x: self.context.get_message(x), self.options))

        buttons = [
            [types.KeyboardButton(text=self.context.get_message("restrictions_skipBtn"))],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)

        if self.hasPoll:
            if self.context.user.restrictions_tags is not None:
                poll_info = await update.bot.send_poll(
                    chat_id=update.getChatId(),
                    question=self.context.get_message("restrictions_tag_text"),
                    options=options,
                    is_anonymous=False,
                    allows_multiple_answers=True,
                    reply_markup=keyboard,
                )
            else:
                poll_info = await update.bot.send_poll(
                    chat_id=update.getChatId(),
                    question=self.context.get_message("restrictions_tag_text"),
                    options=options,
                    is_anonymous=False,
                    allows_multiple_answers=True,
                    reply_markup=types.ReplyKeyboardRemove(),
                )
            self.context.user.active_poll_id = poll_info.poll.id
            self.context.save_to_db()
