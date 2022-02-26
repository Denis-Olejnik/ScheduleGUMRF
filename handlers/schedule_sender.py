from datetime import datetime

from loguru import logger

from data.config import DEBUG_MODE
from database import postgre, get_schedule
# from database.get_user_schedule import get_user_schedule_for_day
from loader import dp

from aiogram import types
from aiogram.utils.exceptions import Unauthorized, BadRequest


async def show_schedule(message: types.Message):
    user_id = None
    try:
        try:
            user_id = message.from_user.id

            # Get user group code:
            user_data = await postgre.execute_read_query(f"SELECT * FROM users WHERE user_id='{user_id}'")
            user_group = f"{user_data[0][2]}_{user_data[0][3]}".replace('-', '_')
            schedule = await get_schedule.get_user_schedule_today(user_group, 1)

            await dp.bot.send_message(chat_id=message.from_user.id, text=schedule, parse_mode=types.ParseMode.HTML)

        except postgre.ps.OperationalError as postgre_error:
            await dp.bot.send_message(chat_id=user_id, text="Database error.")
            logger.exception(postgre_error)

    except (BadRequest, Unauthorized) as aiogram_error:
        if DEBUG_MODE:
            await dp.bot.send_message(chat_id=message.from_user.id,
                                      text=f"{aiogram_error}\n"
                                           f"Please contact the administrator: @RUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUR",
                                      parse_mode=types.ParseMode.HTML)
        logger.exception(aiogram_error)
