from aiogram import Dispatcher, Bot, types
from src.statemachine.StateCacheHolder import StateCacheHolder
from src.bot.Update import Update, Message, PollAnswer
from aiogram import F


class Handler:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self.stateCacheHolder = StateCacheHolder()
        self.register_handlers()

    async def update_handler(self, update: Update):
        chat_id = update.getChatId()
        curState = self.stateCacheHolder.getState(chat_id)
        nextState = curState.goNextState(update)
        await nextState.sendMessage(update)
        self.stateCacheHolder.setState(chat_id, nextState)

    def register_handlers(self):
        @self.dp.poll_answer()
        async def poll_answer_handler(poll: types.PollAnswer):
            update = PollAnswer(self.bot, self.dp, poll)
            await self.update_handler(update)

        @self.dp.message()
        async def message_handler(message: types.Message):
            update = Message(self.bot, self.dp, message)
            await self.update_handler(update)




