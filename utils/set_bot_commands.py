from aiogram import types
from loguru import logger


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("schedule_get", "Получить расписание"),
            types.BotCommand("schedule_edit", "Добавить новое расписание"),
            types.BotCommand("schedule_del", "Удалить расписание")
        ]
    )
    logger.debug("Default commands setup complete!")
