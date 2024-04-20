from src.statemachine import State
from src.statemachine.state import profile
from src.model.Update import Update
from src.model import Tags as TagsModel
from aiogram import types


class FoodPreferencesTagState(State):
    def __init__(self, context):
        super().__init__(context)
        self.options = TagsModel.preferencesTags.copy()
        self.options.append(TagsModel.nothing_tag)
        self.hasPoll = True

    async def process_update(self, update: Update):
        message = update.get_message()

        if (
            self.context.user.preferences_tags is not None
            and message is not None
            and message.text == self.context.get_message("preferences_skipBtn")
        ):
            self.context.set_state(profile.RestrictionsTagState(self.context))
            self.context.save_to_db()
            self.hasPoll = False
            return

        poll_answer = update.get_poll_answer()
        if poll_answer and int(poll_answer.poll_id) == int(self.context.user.active_poll_id):
            self.context.user.preferences_tags = set()
            for option_id in poll_answer.option_ids:
                option_name = self.options[option_id]
                if option_name == TagsModel.nothing_tag:
                    continue
                self.context.user.preferences_tags.add(option_name)
            self.context.set_state(profile.RestrictionsTagState(self.context))
            self.context.save_to_db()
        self.hasPoll = False

    async def send_message(self, update: Update):
        options = list(map(lambda x: self.context.get_message(x), self.options))

        buttons = [
            [types.KeyboardButton(text=self.context.get_message("preferences_skipBtn"))],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)

        if self.hasPoll:
            if self.context.user.preferences_tags is not None:
                poll_info = await update.bot.send_poll(
                    chat_id=update.get_chat_id(),
                    question=self.context.get_message("preferences_tag_text"),
                    options=options,
                    is_anonymous=False,
                    allows_multiple_answers=True,
                    reply_markup=keyboard,
                )
            else:
                poll_info = await update.bot.send_poll(
                    chat_id=update.get_chat_id(),
                    question=self.context.get_message("preferences_tag_text"),
                    options=options,
                    is_anonymous=False,
                    allows_multiple_answers=True,
                    reply_markup=types.ReplyKeyboardRemove(),
                )
            self.context.user.active_poll_id = poll_info.poll.id
            self.context.save_to_db()
