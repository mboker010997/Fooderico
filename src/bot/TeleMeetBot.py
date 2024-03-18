import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from src.bot.Handler import Handler
from src.bot.DBController import DBController
import os

class TelegramBot:
    def __init__(self):
        load_dotenv()
        self.bot = Bot(os.getenv("TOKEN"))
        self.dp = Dispatcher()
        self.handler = Handler(self.bot, self.dp)
        logging.basicConfig(level=logging.INFO)

    async def start_polling(self):
        await self.dp.start_polling(self.bot)


if __name__ == '__main__':
    try:
        dbcontroller = DBController()
        bot = TelegramBot()
        asyncio.run(bot.start_polling())
    except Exception as _ex:
        print(_ex)
    finally:
        if dbcontroller.connection:
            dbcontroller.connection.commit()
            dbcontroller.connection.close()
