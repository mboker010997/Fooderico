from aiogram import Dispatcher

from state.Start import start
from state.Help import help


class StateMachine:
    def __init__(self, dp: Dispatcher):
        self.dp = dp
        self.register_handlers()

    def register_handlers(self):
        start(self.dp)
        help(self.dp)
