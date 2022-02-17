from aiogram import Dispatcher, types
from loguru import logger


async def cmd_start(message: types.Message):
    logger.info(f"User @{message.from_user.username} [{message.from_user.id}] start conversation with bot!")


def register_handlers_base(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'])
    logger.debug("Handler registered!")
