
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import callback_data
from aiogram.utils.callback_data import CallbackData


schedule_data = CallbackData("schedule", 'field', 'value')

btn_schedule_get_next_day = InlineKeyboardButton("➡", callback_data=schedule_data.new(
    field='get_schedule', value='get_schedule_next_day'))
btn_schedule_refresh = InlineKeyboardButton("🔄", callback_data=schedule_data.new(
    field='refresh', value='refresh_schedule'))
btn_schedule_get_prev_day = InlineKeyboardButton('⬅', callback_data=schedule_data.new(
    field='get_schedule', value='get_schedule_next_day'))

kb_schedule = InlineKeyboardMarkup().row(btn_schedule_get_prev_day, btn_schedule_refresh, btn_schedule_get_next_day)
