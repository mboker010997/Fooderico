from aiogram import Dispatcher, types
from aiogram.filters.command import Command

from state.InitialState import InitialState


class Handler:
    def __init__(self, bot, dp):
        self.bot = bot
        self.dp = dp
        self.state = InitialState() # change to map: chatId -> State
        self.register_handlers()

    def register_handlers(self):
        commands = ["start", "help"] # move to BotConfig
        for command in commands:
            @self.dp.message(Command(command))
            async def command_handler(message: types.Message):
                await self.state.parseInput(message) # is self.dp in args, is async
                await self.state.processUpdate()

