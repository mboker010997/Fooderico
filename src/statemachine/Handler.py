from aiogram import Dispatcher, types
from aiogram.filters.command import Command

from state.InitialState import InitialState
from StateCacheHolder import StateCacheHolder
import logging

class Handler:
    def __init__(self, bot, dp):
        self.bot = bot
        self.dp = dp
        self.stateCacheHolder = StateCacheHolder()
        self.register_handlers()

    def register_handlers(self):
        commands = ["start"] # move to BotConfig

        @self.dp.message(Command("start"))
        async def start_handler(message: types.Message):
            curState = InitialState(self.bot, self.dp)
            self.stateCacheHolder.setState(message.chat.id, curState)
            curState = self.stateCacheHolder.getState(message.chat.id)
            nextState = curState.goNextState(message)
            await nextState.sendMessage(message)
            self.stateCacheHolder.setState(message.chat.id, nextState)

        for command in commands:
            @self.dp.message(Command(command))
            async def command_handler(message: types.Message):
                curState = self.stateCacheHolder.getState(message.chat.id)
                nextState = curState.goNextState(message)
                await nextState.sendMessage(message)
                self.stateCacheHolder.setState(message.chat.id, nextState)
