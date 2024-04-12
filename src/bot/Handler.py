from aiogram import Dispatcher, Bot, types
from src.model import Update, Message, PollAnswer, CallbackQuery
import logging
from src.model import StateUpdater
from typing import List
from aiogram import F
from aiogram.types import InputMediaPhoto, InputMedia, ContentType as CT, Message as mes
from src.statemachine.state import chat


class Handler:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self.register_handlers()

    async def update_handler(self, update: Update):
        chat_id = update.getChatId()
        sentMessage = StateUpdater.getSentMessage(chat_id)
        if sentMessage is not None:
            await self.bot.delete_message(chat_id=sentMessage.chat.id, message_id=sentMessage.message_id)

        curState = StateUpdater.getState(chat_id)
        nextState = curState.goNextState(update)
        try:
            newMessage = await nextState.sendMessage(update)
            StateUpdater.setSentMessage(chat_id, newMessage)
        except Exception as exc:
            logging.exception(exc)

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

        @self.dp.callback_query(F.data.startswith("go_anon_chat_"))
        async def transition_to_anon_chat(callback: types.CallbackQuery):
            chat_id = callback.from_user.id
            update = CallbackQuery(self.bot, self.dp, callback)
            context = StateUpdater.getContext(chat_id)
            if context is None:
                return

            expected_prefix = "go_anon_chat_"
            other_chat_id = int(callback.data[len(expected_prefix):])
            context.other_chat_id = other_chat_id
            context.setState(chat.ChatState(context))
            context.saveToDb()

            await context.state.sendMessage(update)
