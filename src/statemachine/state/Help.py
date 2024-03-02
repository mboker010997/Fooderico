from aiogram import Dispatcher, types
from aiogram.filters.command import Command


def help(dp: Dispatcher):
    @dp.message(Command("help"))
    async def cmd_help(message: types.Message):
        await message.answer("How can I help you?")
