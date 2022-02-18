import random
import secrets
from datetime import datetime

from aiogram import Dispatcher, types
from loguru import logger

from data import texts
from data.config import DEBUG_MODE
from database import postgre
from handlers.user_survey import sm_start
from keyboards import user_inline_keyboard
from loader import dp


async def cmd_start(message: types.Message):
    await message.answer(text=texts.on_start_command, reply_markup=user_inline_keyboard)
    logger.info(f"User @{message.from_user.username} [{message.from_user.id}] start conversation with bot!")


async def show_schedule(message: types.Message):
    user_id = message.from_user.id
    user_has_registered = await postgre.has_user_registered(user_id)

    if not user_has_registered:
        await sm_start(message)
        logger.warning(F"User {message.from_user.username} [{message.from_user.id}] not founded in DB!")
    else:
        try:
            await message.answer("Получаю расписание")
            user_data = await postgre.execute_read_query(f"SELECT * FROM users WHERE user_id = {user_id}")
            user_data = user_data[0]
            user_group = f"{user_data[1]}_{user_data[2]}"

            day_of_week = datetime.today().isocalendar()[2]
            current_week = datetime.today().isocalendar()[1]
            fractional = int(current_week) % 2  # Расчёт числителя или знаменателя

            # TODO: Выделять текущую пару относительно времени (9.30 < x < 11.15)

            ###################################################### TESTS:
            if DEBUG_MODE:
                week_day = secrets.randbelow(5)
                fractional = random.randrange(0, 2)
                user_group = "IS_31_" + str(random.randrange(1, 3))
                print(f"group={user_group}, fractional={fractional}, day of the week = {week_day}")

                schedule = await postgre.get_user_schedule_for_day(user_group, week_day, fractional)
                schedule = schedule[0][0]

                schedule = f"\nГруппа: {user_group}, День недели: {week_day}, Дробь: {fractional}\n\n" + schedule

            ###################################################### TESTS:
                await dp.bot.send_message(chat_id=user_id, text=schedule)

        except (Exception) as err:
            logger.exception(err)


def register_handlers_base(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_callback_query_handler(show_schedule)
    logger.debug("Handler registered!")
