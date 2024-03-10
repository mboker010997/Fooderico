from aiogram import Dispatcher, types
from aiogram.filters.command import Command

from src.statemachine.state.InitialState import InitialState
from src.statemachine.StateCacheHolder import StateCacheHolder
import logging


class Handler:
    def __init__(self, bot, dp):
        self.bot = bot
        self.dp = dp
        self.stateCacheHolder = StateCacheHolder()
        self.register_handlers()

    def register_handlers(self):
        @self.dp.message()
        async def message_handler(message: types.Message):
            curState = self.stateCacheHolder.getState(message.chat.id)
            nextState = curState.goNextState(message)
            await nextState.sendMessage(message, self.bot, self.dp)
            self.stateCacheHolder.setState(message.chat.id, nextState)
