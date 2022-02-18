
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# SUB GROUP CODE:
btn_subgroup_code_first = InlineKeyboardButton("Первая", callback_data="subgroup_1")
btn_subgroup_code_second = InlineKeyboardButton("Вторая", callback_data="subgroup_2")

keyboard_subgroup_code = InlineKeyboardMarkup().add(btn_subgroup_code_first, btn_subgroup_code_second)


# GROUP LEADER
btn_leader_true = InlineKeyboardButton("Да", callback_data="is_leader_true")
btn_leader_false = InlineKeyboardButton("Нет", callback_data="is_leader_true")

keyboard_group_leader = InlineKeyboardMarkup().add(btn_leader_true, btn_leader_false)

# ALL IS CORRECT:
btn_all_correct = InlineKeyboardButton("Всё верно", callback_data="survey_results_correct")
btn_reset = InlineKeyboardButton("Исправить", callback_data="reset_survey_results")

keyboard_results = InlineKeyboardMarkup().add(btn_all_correct, btn_reset)
