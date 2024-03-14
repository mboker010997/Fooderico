import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from src.bot.Handler import Handler
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
    bot = TelegramBot()
    asyncio.run(bot.start_polling())
