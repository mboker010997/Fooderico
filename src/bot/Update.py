import logging
from aiogram import Bot, Dispatcher, types
from abc import abstractmethod


class Update:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp

    @abstractmethod
    def getChatId(self):
        pass

    def getMessage(self):
        pass

    def getPollAnswer(self):
        pass


class Message(Update):
    def __init__(self, bot: Bot, dp: Dispatcher, message: types.Message):
        super().__init__(bot, dp)
        self.message = message

    def getChatId(self):
        return self.message.chat.id

    def getMessage(self):
        return self.message


class PollAnswer(Update):
    def __init__(self, bot: Bot, dp: Dispatcher, poll: types.PollAnswer):
        super().__init__(bot, dp)
        self.poll = poll

    def getChatId(self):
        return self.poll.user.id

    def getPollAnswer(self):
        return self.poll