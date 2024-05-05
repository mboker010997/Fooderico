import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from src import bot
import os
from src.model.chat import create_message_table
from src.model import Localization
from src.bot.middlewares import AlbumMiddleware
import src.model.chat as chat_model
from src.admin import crud as admin


class TelegramBot:
    def __init__(self):
        load_dotenv()
        self.bot = Bot(os.getenv("TOKEN"))
        self.dp = Dispatcher()
        self.message_storage = chat_model.MessageStorage()
        self.handler = bot.Handler(self)
        logging.basicConfig(level=logging.INFO)

    async def start_polling(self):
        await self.dp.start_polling(self.bot)


if __name__ == "__main__":
    try:
        dbcontroller = bot.DBController()
        Localization.load_info()
        admin.create_admin_table()
        bot = TelegramBot()
        bot.dp.message.middleware(AlbumMiddleware())
        create_message_table()
        asyncio.run(bot.start_polling())

        if dbcontroller.connection:
            dbcontroller.connection.commit()
            dbcontroller.connection.close()
    except Exception:
        logging.exception("Main (TeleMeetBot)")
