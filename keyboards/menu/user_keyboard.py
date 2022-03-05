from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from data.menu_texts import text_show_schedule, text_open_user_settings, text_about_software

btn_show_schedule_inline = InlineKeyboardButton(text="Посмотреть расписание", callback_data="btn_show_schedule_inline")
btn_test = InlineKeyboardButton(text='test', callback_data="btn_test")
KEYB_SCHEDULE = InlineKeyboardMarkup().add(btn_show_schedule_inline).add(btn_test)


# User main menu buttons:
btn_show_schedule = KeyboardButton(text=text_show_schedule)
btn_open_user_settings = KeyboardButton(text=text_open_user_settings)
btn_show_about_software = KeyboardButton(text=text_about_software)
USER_MENU = ReplyKeyboardMarkup(resize_keyboard=True).row(btn_show_schedule,
                                                          btn_open_user_settings,
                                                          btn_show_about_software)

