from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# Generate inline keyboard:
btn_show_schedule_inline = InlineKeyboardButton(text="Посмотреть расписание", callback_data="btn_show_schedule_inline")
btn_test = InlineKeyboardButton(text='test', callback_data="btn_test")
KEYB_SCHEDULE = InlineKeyboardMarkup().add(btn_show_schedule_inline).add(btn_test)


# User main menu buttons:
btn_show_schedule = KeyboardButton(text='Расписание 📅')
btn_show_news = KeyboardButton(text='Новости 📰')
btn_open_user_settings = KeyboardButton(text='Настройки ⚙')
USER_MENU = ReplyKeyboardMarkup(resize_keyboard=True).row(btn_show_schedule, btn_show_news, btn_open_user_settings)