import logging
from aiogram import Bot, Dispatcher, types
from abc import abstractmethod


class Update:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
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
    def __init__(self, bot: Bot, dp: Dispatcher, message: types.Message):
        super().__init__(bot, dp)
        self.message = message

    def getChatId(self):
        return self.message.from_user.id

    def getMessage(self) -> types.Message:
        return self.message


class PollAnswer(Update):
    def __init__(self, bot: Bot, dp: Dispatcher, poll: types.PollAnswer):
        super().__init__(bot, dp)
        self.poll = poll

    def getChatId(self):
        return self.poll.user.id

    def getPollAnswer(self) -> types.PollAnswer:
        return self.poll


class CallbackQuery(Update):
    def __init__(
        self, bot: Bot, dp: Dispatcher, callback_query: types.CallbackQuery
    ):
        super().__init__(bot, dp)
        self.callback_query = callback_query

    def getChatId(self):
        return self.callback_query.from_user.id

    def getCallbackQuery(self) -> types.CallbackQuery:
        return self.callback_query
