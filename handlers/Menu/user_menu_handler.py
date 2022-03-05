from aiogram.types import Message
from loguru import logger
from handlers.schedule_sender import show_schedule
from loader import dp


async def menu_show_schedule(message: Message):
    await show_schedule(message)


async def register_handlers_user_menu():
    dp.register_message_handler(menu_show_schedule, text='Расписание 📅')
    logger.debug("Commands handler registered!")
