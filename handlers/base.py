import logging

from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from loader import dp


@dp.message_handler(CommandStart())
async def cmd_start(message: types.Message):
    logging.info(f"User {message.from_user.id} start conversation with bot!")
