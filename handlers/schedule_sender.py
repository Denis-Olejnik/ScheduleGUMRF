from datetime import datetime

import pytz
from aiogram.types import CallbackQuery
from loguru import logger

from data.config import DEBUG_MODE
from database import postgre, get_schedule
from keyboards import kb_schedule
from keyboards.shedule_keyboard import schedule_data
from loader import dp

from aiogram import types, Dispatcher
from aiogram.utils.exceptions import Unauthorized, BadRequest, MessageNotModified


async def show_schedule(message: types.Message):
    user_id = None
    try:
        try:
            user_id = message.from_user.id

            # Get user group code:
            user_data = await postgre.execute_read_query(f"SELECT * FROM users WHERE user_id='{user_id}'")
            user_group = f"{user_data[0][2]}_{user_data[0][3]}".replace('-', '_')

            schedule = await get_schedule.get_user_schedule_today(user_group, datetime.now(pytz.timezone('Europe/Moscow')).isoweekday())
            # if answer contains any data (first val of dict = True)
            if schedule[0]:
                await dp.bot.send_message(chat_id=message.from_user.id, text=schedule[1],
                                          reply_markup=kb_schedule, parse_mode=types.ParseMode.HTML)
            else:
                await dp.bot.send_message(chat_id=message.from_user.id, text=schedule[1],
                                          reply_markup=kb_schedule, parse_mode=types.ParseMode.HTML)

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


async def update_schedule_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    message_id = query.message.message_id
    user_group = str()

    try:
        # Get user group:
        user_data = await postgre.execute_read_query(f"SELECT * FROM users WHERE user_id='{user_id}'")
        user_group = f"{user_data[0][2]}_{user_data[0][3]}".replace('-', '_')
    except (postgre.ps.OperationalError, postgre.ps.DataError) as database_error:
        logger.exception(database_error)
        if DEBUG_MODE:
            dp.bot.send_message(chat_id=user_id, message_id=database_error)

    try:
        new_schedule = await get_schedule.get_user_schedule_today(user_group, datetime.now(pytz.timezone('Europe/Moscow')).isoweekday())
        message_updated = await dp.bot.edit_message_text(chat_id=user_id, text=new_schedule[1], message_id=message_id, reply_markup=kb_schedule, parse_mode=types.ParseMode.HTML)
        if message_updated:
            await query.answer("Расписание обновлено!")
            logger.info("Schedule message is updated!")
        else:
            logger.info("Updated message equals old message")
            await query.answer("Расписание не изменилось")
    except MessageNotModified as update_error:
        await query.answer("Расписание не изменилось")
    except (BadRequest, Unauthorized) as aiogram_error:
        logger.exception(aiogram_error)
        if DEBUG_MODE:
            dp.bot.send_message(chat_id=user_id, message_id=aiogram_error)


def register_handlers_inline_keyb(dp: Dispatcher):
    dp.register_callback_query_handler(update_schedule_message, schedule_data.filter(field="refresh_schedule"))
    logger.debug("Schedule inline keyboards has registered!")
