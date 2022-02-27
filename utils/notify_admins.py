from aiogram import Dispatcher
from loguru import logger

from data.config import TELEGRAM_ADMINS, TELEGRAM_NOTIFY_ADMIN


async def on_startup_notify(dp: Dispatcher):
    if TELEGRAM_NOTIFY_ADMIN:
        for admin in TELEGRAM_ADMINS:
            try:
                await dp.bot.send_message(admin, "Бот запущен\!")
                logger.info(f"Admin {admin} received a notification!!")

            except Exception as error:
                logger.exception(error)
    logger.info("Bot started!")
