from aiogram import Dispatcher
from loguru import logger

from data.config import TELEGRAM_ADMINS


async def on_startup_notify(dp: Dispatcher):
    for admin in TELEGRAM_ADMINS:
        try:
            await dp.bot.send_message(admin, "Бот запущен!")
            logger.info(f"Admin {admin} got his notify!")

        except Exception as error:
            logger.exception(error)
    logger.info("Bot started!")
