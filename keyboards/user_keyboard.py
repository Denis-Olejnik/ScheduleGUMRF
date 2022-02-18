from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Generate inline keyboard:
btn_show_schedule = InlineKeyboardButton(text="Посмотреть расписание", callback_data="btn_show_schedule")

user_inline_keyboard = InlineKeyboardMarkup().add(btn_show_schedule)



