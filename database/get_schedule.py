from datetime import datetime

import pytz
from aiogram.utils.exceptions import Unauthorized, BadRequest
from loguru import logger

from data import texts
from database import postgre


async def time_in_range(start_time, end_time, current_time) -> bool:
    if start_time <= end_time:
        return start_time <= current_time <= end_time
    else:
        return start_time <= current_time or current_time <= end_time


async def is_numerator() -> bool:
    """
    The function returns the week type - numerator or denominator.

    :return: TRUE = numerator, otherwise it returns false
    """
    current_week = datetime.now().isocalendar()[1]
    if current_week % 2:
        return True
    else:
        return False

async def get_remaining_lec_time(lecture_num, lec_time, current_time) -> str:
    return '123'

async def format_schedule_time(schedule: tuple = None):
    """
    Converts to a format suitable for user output
    :return:
    """
    lines = schedule[0].split('\n')
    schedule_dict = dict()
    result = str()

    lec_time = {
        'lecture_1': {'start': '09:30', 'end': '11:05'},
        'lecture_2': {'start': '11:15', 'end': '12:50'},
        'lecture_3': {'start': '13:35', 'end': '15:10'},
        'lecture_4': {'start': '15:20', 'end': '16:55'}
    }

    current_time = datetime.now(pytz.timezone('Europe/Moscow')).strftime("%H:%M")

    # Transformation from str to dictionary and format text:
    for index, line in enumerate(lines, 1):
        schedule_dict[f"lecture_{index}"] = line

        lec_start_time = lec_time[f"lecture_{index}"]['start']
        lec_end_time = lec_time[f"lecture_{index}"]['end']

        if await time_in_range(lec_start_time, lec_end_time, current_time):
            schedule_dict[f"lecture_{index}"] = f"<b>>> {line}</b>"

        _lec_index = f"lecture_{index}"
        result += f"{schedule_dict[_lec_index]}\n"
    else:
        # result += await get_remaining_lec_time()
        pass
    return result


async def get_user_schedule_today(group_code: str, week_day: int = None) -> tuple[bool, str]:
    """
    Runs a query to the database and gets the full schedule for today for the specified group.
    :param group_code: User's group membership
    :param week_day: The current day of the week, where Monday = 1
    :return:
    """
    day_of_week = week_day or '1'
    try:
        if await is_numerator():
            query = f"SELECT schedule_numerator FROM schedule WHERE group_code='{group_code}' and week_day='{day_of_week}'"
        else:
            query = f"SELECT schedule_denominator FROM schedule WHERE group_code='{group_code}' and week_day='{day_of_week}'"

        schedule = await postgre.execute_read_query(query)
        if len(schedule) > 0:
            schedule_formatted = await format_schedule_time(schedule[0])
            return True, schedule_formatted
        else:
            schedule_formatted = texts.TEXT_TODAY_SCHEDULE_NOT_FOUND
            return False, schedule_formatted

    except (postgre.ps.OperationalError, postgre.ps.DataError) as database_error:
        logger.exception(database_error)
    except (BadRequest, Unauthorized) as aiogram_error:
        logger.exception(aiogram_error)

