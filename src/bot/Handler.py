from aiogram import Dispatcher, Bot, types
from src.model import Update, Message, PollAnswer
import logging
from src.model import StateUpdater
from typing import List
from aiogram import F
from aiogram.types import InputMediaPhoto, InputMedia, ContentType as CT, Message as mes

class Handler:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self.register_handlers()

    async def update_handler(self, update: Update):
        chat_id = update.getChatId()
        curState = StateUpdater.getState(chat_id)
        nextState = curState.goNextState(update)
        try:
            await nextState.sendMessage(update)
        except Exception as exc:
            logging.error(exc)

    def register_handlers(self):
        @self.dp.message(F.content_type.in_([CT.PHOTO]))
        async def handle_albums(message: mes, album: List[mes] = None):
            update = Message(self.bot, self.dp, message)
            update.album = album
            await self.update_handler(update)

        @self.dp.poll_answer()
        async def poll_answer_handler(poll: types.PollAnswer):
            update = PollAnswer(self.bot, self.dp, poll)
            await self.update_handler(update)

        @self.dp.message()
        async def message_handler(message: mes):
            update = Message(self.bot, self.dp, message)
            await self.update_handler(update)




