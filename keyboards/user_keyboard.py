from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Generate inline keyboard:
btn_show_schedule = InlineKeyboardButton(text="Посмотреть расписание", callback_data="btn_show_schedule")
btn_test = InlineKeyboardButton(text='test', callback_data="btn_test")
KEYB_SCHEDULE = InlineKeyboardMarkup().add(btn_show_schedule).add(btn_test)



