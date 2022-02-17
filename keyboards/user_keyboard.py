from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Generate markup keyboard:
btn_show_menu = KeyboardButton("Меню")

user_markup_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
user_markup_keyboard.add(btn_show_menu)


# Generate inline keyboard:
btn_show_schedule = InlineKeyboardButton("Посмотреть расписание", callback_data="btn_show_schedule")

user_inline_keyboard = InlineKeyboardMarkup().add(btn_show_schedule)
