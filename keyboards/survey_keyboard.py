from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

btn_subgroup_code_first = InlineKeyboardButton("Первая", callback_data="subgroup_first")
btn_subgroup_code_second = InlineKeyboardButton("Вторая", callback_data="subgroup_second")

keyboard_subgroup_code = InlineKeyboardMarkup().add(btn_subgroup_code_first, btn_subgroup_code_second)

