from aiogram import Dispatcher, types
from aiogram.filters.command import Command


def start(dp: Dispatcher):
    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        await message.answer("Hello!")
