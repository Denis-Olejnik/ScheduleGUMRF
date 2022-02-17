import logging

from aiogram import Dispatcher

from data.config import TELEGRAM_ADMINS


async def on_startup_notify(dp: Dispatcher):
    for admin in TELEGRAM_ADMINS:
        try:
            await dp.bot.send_message(admin, "Бот запущен!")
            logging.info("Bot launched successfully!")

        except Exception as error:
            logging.exception(error)
