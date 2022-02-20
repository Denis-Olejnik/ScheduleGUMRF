from aiogram import executor

from data import config
from database import postgre
from handlers import commands, user_survey
from loader import dp, bot

from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands

commands.register_handlers_base(dp)
user_survey.register_handlers_sm_user(dp)
# schedule.register_callback_query_handler(dp)

import logging
logging.basicConfig(level=logging.DEBUG)


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)
    await postgre.create_connection()

    if not config.RUN_LOCAL:
        await bot.set_webhook(config.POSTGRES_URI)


async def on_shutdown(dispatcher):
    if not config.RUN_LOCAL:
        await bot.delete_webhook()


if __name__ == "__main__":
    if config.RUN_LOCAL:
        executor.start_polling(dispatcher=dp, on_startup=on_startup, skip_updates=True)
    else:
        executor.start_webhook(dispatcher=dp,
                               webhook_path="",
                               on_startup=on_startup,
                               on_shutdown=on_shutdown,
                               skip_updates=True,
                               host="0.0.0.0",
                               port=int(5000)
                               )
