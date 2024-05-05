from abc import abstractmethod
from aiogram import types


class Update:
    def __init__(self, telebot):
        self.bot = telebot.bot
        self.dp = telebot.dp
        self.message_storage = telebot.message_storage
        self.album = None
        self.voice_id = None
        self.video_note_id = None

    @abstractmethod
    def get_chat_id(self):
        pass

    def get_message(self) -> types.Message:
        pass

    def get_poll_answer(self) -> types.PollAnswer:
        pass

    def get_callback_query(self) -> types.CallbackQuery:
        pass


class Message(Update):
    def __init__(self, telebot, message: types.Message):
        super().__init__(telebot)
        self.message = message

    def get_chat_id(self):
        return self.message.from_user.id

    def get_message(self) -> types.Message:
        return self.message


class PollAnswer(Update):
    def __init__(self, telebot, poll: types.PollAnswer):
        super().__init__(telebot)
        self.poll = poll

    def get_chat_id(self):
        return self.poll.user.id

    def get_poll_answer(self) -> types.PollAnswer:
        return self.poll


class CallbackQuery(Update):
    def __init__(self, telebot, callback_query: types.CallbackQuery):
        super().__init__(telebot)
        self.callback_query = callback_query

    def get_chat_id(self):
        return self.callback_query.from_user.id

    def get_callback_query(self) -> types.CallbackQuery:
        return self.callback_query
