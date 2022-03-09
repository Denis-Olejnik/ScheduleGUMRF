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


async def get_hours_mins(time: datetime.time) -> dict:
    hours = time.seconds // 3600
    minutes = (time.seconds // 60) % 60
    result = {"hours": hours, "mins": minutes}
    return result


async def get_remaining_time(lecture, current_time) -> str:
    lecture_starts_in = datetime.strptime(lecture['start'], "%H:%M")
    lecture_end_in = datetime.strptime(lecture['end'], "%H:%M")
    current_time = datetime.strptime(current_time, "%H:%M")

    if current_time < lecture_starts_in:
        delta_time = lecture_starts_in - current_time
        remaining_time = await get_hours_mins(delta_time)
        return f"Начало пары через: {remaining_time.get('hours')} ч. {remaining_time.get('mins')} мин."
    else:
        delta_time = lecture_end_in - current_time
        remaining_time = await get_hours_mins(delta_time)
        return f"До конца пары осталось: {remaining_time.get('hours')} ч. {remaining_time.get('mins')} мин."


async def format_schedule_time(schedule: tuple = None):
    """
    Converts to a format suitable for user output
    :return:
    """
    lines = schedule[0].split('\n')
    schedule_dict = dict()
    result = str()
    time_tmp = str()

    lec_time = {
        'lecture_1': {'start': '09:30', 'end': '11:05'},
        'lecture_2': {'start': '11:15', 'end': '12:50'},
        'lecture_3': {'start': '13:35', 'end': '15:10'},
        'lecture_4': {'start': '15:20', 'end': '16:55'}
    }

    current_time = datetime.now(pytz.timezone('Europe/Moscow')).strftime("%H:%M")
    # current_time = datetime.now(pytz.timezone('US/Alaska')).strftime("%H:%M")

    # Transformation from str to dictionary and format text:
    for index, line in enumerate(lines, 1):
        schedule_dict[f"lecture_{index}"] = line

        lec_start_time = lec_time[f'lecture_{index}']['start']
        lec_end_time = lec_time[f'lecture_{index}']['end']

        if await time_in_range(lec_start_time, lec_end_time, current_time):
            current_lec = lec_time[f"lecture_{index}"]
            # Outline current line:
            schedule_dict[f"lecture_{index}"] = f"<b>>> {line}</b>"
            time_tmp = await get_remaining_time(current_lec, current_time)
        _lec_index = f"lecture_{index}"
        result += f"{schedule_dict[_lec_index]}\n"
    else:
        result += "\n" + time_tmp

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
            query = f"SELECT schedule_1 FROM schedule WHERE group_code='{group_code}' and week_day='{day_of_week}'"
        else:
            query = f"SELECT schedule_0 FROM schedule WHERE group_code='{group_code}' and week_day='{day_of_week}'"

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

