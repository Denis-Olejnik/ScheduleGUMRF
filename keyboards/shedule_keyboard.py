
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


schedule_data = CallbackData("schedule", 'field', 'value')

btn_schedule_get_next_day = InlineKeyboardButton("Следующий день", callback_data=schedule_data.new(
    field='get_schedule', value='get_schedule_next_day'))
btn_schedule_get_prev_day = InlineKeyboardButton('Предыдущий день', callback_data=schedule_data.new(
    field='get_schedule', value='get_schedule_next_day'))

kb_schedule = InlineKeyboardMarkup().add(btn_schedule_get_next_day).add(btn_schedule_get_prev_day)
