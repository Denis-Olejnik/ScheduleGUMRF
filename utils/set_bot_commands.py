from aiogram import types
from loguru import logger


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("get", "Получить расписание"),
            types.BotCommand("add", "Добавить новое расписание"),
            types.BotCommand("del", "Удалить расписание")
        ]
    )
    logger.debug("Default commands setup complete!")
