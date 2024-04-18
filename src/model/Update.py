import logging
from aiogram import Bot, Dispatcher, types
from abc import abstractmethod


class Update:
    def __init__(self, telebot):
        self.bot = telebot.bot
        self.dp = telebot.dp
        self.message_storage = telebot.message_storage
        self.album = None

    @abstractmethod
    def getChatId(self):
        pass

    def getMessage(self) -> types.Message:
        pass

    def getPollAnswer(self) -> types.PollAnswer:
        pass

    def getCallbackQuery(self) -> types.CallbackQuery:
        pass


class Message(Update):
    def __init__(self, telebot, message: types.Message):
        super().__init__(telebot)
        self.message = message

    def getChatId(self):
        return self.message.from_user.id

    def getMessage(self) -> types.Message:
        return self.message


class PollAnswer(Update):
    def __init__(self, telebot, poll: types.PollAnswer):
        super().__init__(telebot)
        self.poll = poll

    def getChatId(self):
        return self.poll.user.id

    def getPollAnswer(self) -> types.PollAnswer:
        return self.poll


class CallbackQuery(Update):
    def __init__(
        self, telebot, callback_query: types.CallbackQuery
    ):
        super().__init__(telebot)
        self.callback_query = callback_query

    def getChatId(self):
        return self.callback_query.from_user.id

    def getCallbackQuery(self) -> types.CallbackQuery:
        return self.callback_query
