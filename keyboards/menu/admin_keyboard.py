from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


# User main menu buttons:
btn_admin_item_1 = KeyboardButton(text='ADMIN_1')
btn_admin_item_2 = KeyboardButton(text='ADMIN_2')
btn_admin_item_3 = KeyboardButton(text='ADMIN_3')
btn_admin_back = KeyboardButton(text='ADMIN_BACK')
ADMIN_MENU = ReplyKeyboardMarkup(resize_keyboard=True).row(
    btn_admin_item_1, btn_admin_item_2, btn_admin_item_3).add(
    btn_admin_back)

