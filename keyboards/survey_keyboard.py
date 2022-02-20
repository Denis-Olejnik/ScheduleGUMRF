
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# START USER SURVEY:
from aiogram.utils.callback_data import CallbackData
#
# # btn_start_user_survey = InlineKeyboardButton("Пройти опрос", callback_data="start_user_survey")
# #
# # keyboard_start_survey = InlineKeyboardMarkup().add(btn_start_user_survey)
#
# # SUB GROUP CODE:
# btn_subgroup_code_first = InlineKeyboardButton("Первая", callback_data="user_subgroup_1")
# btn_subgroup_code_second = InlineKeyboardButton("Вторая", callback_data="user_subgroup_2")
#
# keyboard_subgroup_code = InlineKeyboardMarkup().add(btn_subgroup_code_first, btn_subgroup_code_second)
#
#
# # ALL IS CORRECT:
# btn_all_correct = InlineKeyboardButton("Всё верно", callback_data="survey_results_correct")
# btn_reset = InlineKeyboardButton("Исправить", callback_data="reset_survey_results")
#
# keyboard_results = InlineKeyboardMarkup().add(btn_all_correct, btn_reset)


survey_cb = CallbackData('survey', 'field', 'value')

# START USER SURVEY:
btn_start_user_survey = InlineKeyboardButton("START SURVEY", callback_data=survey_cb.new(field="StartUserSurvey", value="True"))
kb_start_user_survey = InlineKeyboardMarkup().add(btn_start_user_survey)

# GROUP:
btn_survey_group_one = InlineKeyboardButton("IS-31", callback_data=survey_cb.new(field="SurveyGroupName", value="31"))
btn_survey_group_two = InlineKeyboardButton("IS-32", callback_data=survey_cb.new(field="SurveyGroupName", value="32"))
btn_survey_group_three = InlineKeyboardButton("IS-33", callback_data=survey_cb.new(field="SurveyGroupName", value="33"))
kb_survey_group = InlineKeyboardMarkup().row(btn_survey_group_one, btn_survey_group_two, btn_survey_group_three)

# SUBGROUP:
btn_survey_subgroup_one = InlineKeyboardButton("First", callback_data=survey_cb.new(field="UserSurveySubgroup", value="subgroup_one"))
btn_survey_subgroup_two = InlineKeyboardButton("Second", callback_data=survey_cb.new(field="UserSurveySubgroup", value="subgroup_two"))
kb_survey_subgroup = InlineKeyboardMarkup().row(btn_survey_subgroup_one, btn_survey_subgroup_two)

# CONFIRMATION:
btn_survey_correct_true = InlineKeyboardButton("True", callback_data=survey_cb.new(field="SurveyCorrect", value="True"))
btn_survey_correct_false = InlineKeyboardButton("False", callback_data=survey_cb.new(field="SurveyCorrect", value="False"))
kb_survey_correct = InlineKeyboardMarkup().row(btn_survey_correct_true, btn_survey_correct_false)
