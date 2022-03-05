from aiogram import Dispatcher
from aiogram.types import Message
from loguru import logger

from data import text_show_schedule, text_open_user_settings
from handlers.schedule_sender import show_schedule
from loader import dp


async def menu_show_schedule(message: Message):
    await show_schedule(message)


async def menu_open_settings(message: Message):
    await message.answer('user settings')


def register_handlers_user_menu(dp: Dispatcher):
    dp.register_message_handler(menu_show_schedule, text=text_show_schedule)
    dp.register_message_handler(menu_open_settings, text=text_open_user_settings)
    logger.debug("Commands handler registered!")
