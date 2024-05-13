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
from src.bot.config import main_admin


class TelegramBot:
    def __init__(self):
        load_dotenv()
        self.bot = Bot(token="6828269667:AAFr1c6IuDeuyWJnMJUG17ivPkbdIisLEA0")
        # self.bot = Bot(os.getenv("TOKEN"))
        self.dp = Dispatcher()
        self.message_storage = chat_model.MessageStorage()
        self.handler = bot.Handler(self)
        logging.basicConfig(level=logging.INFO)

    async def start_polling(self):
        try:
            await self.dp.start_polling(self.bot)
        except Exception as e:
            logging.exception("An error occurred while polling: %s", e)
            admins = bot.DBController().get_all_admins()
            for id in admins:
                await self.bot.send_message(id, f"An error occurred in Main (TeleMeetBot): {e}")


if __name__ == "__main__":
    try:
        dbcontroller = bot.DBController()
        Localization.load_info()
        # create admin table and add main admins
        bot.DBController().create_admin_table()
        for admin in main_admin:
            bot.DBController().add_admin(admin)

        bot = TelegramBot()
        bot.dp.message.middleware(AlbumMiddleware())
        create_message_table()
        asyncio.run(bot.start_polling())

        if dbcontroller.connection:
            dbcontroller.connection.commit()
            dbcontroller.connection.close()
    except Exception:
        logging.exception("Main (TeleMeetBot)")
