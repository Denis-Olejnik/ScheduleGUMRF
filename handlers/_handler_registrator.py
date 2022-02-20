from aiogram import Dispatcher
from loguru import logger

from handlers.commands import cmd_start
from handlers.schedule import show_schedule


def register_handlers_base(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'])
    logger.debug("Commands handler registered!")


def register_callback_query_handler(dp: Dispatcher):
    dp.register_callback_query_handler(show_schedule, text="show_user_schedule")