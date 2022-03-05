from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


schedule_data = CallbackData("schedule", 'field', 'value')


btn_schedule_refresh = InlineKeyboardButton("🔄", callback_data=schedule_data.new(
    field='refresh_schedule', value='refresh_schedule'))
btn_schedule_get_next = InlineKeyboardButton("На завтра", callback_data=schedule_data.new(
    field='get_next', value='get_for_next_day'))

kb_schedule = InlineKeyboardMarkup().add(btn_schedule_refresh, btn_schedule_get_next)
