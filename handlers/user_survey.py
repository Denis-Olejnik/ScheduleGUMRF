from datetime import datetime

import pytz
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.utils.exceptions import Unauthorized, BadRequest
from loguru import logger

from data import TEXT_SM_USER_GROUP_NAME, TEXT_SM_USER_SUBGROUP_CODE, texts, TEXT_USER_NOT_FOUND_IN_DB
from data.config import DEBUG_MODE, SAVE_TO_DB

from database import postgre

from keyboards.survey_keyboard import survey_cb, kb_survey_correct, kb_survey_subgroup
from loader import dp


class FSMUserSurvey(StatesGroup):
    user_id = State()

    username = State()
    group_name = State()
    subgroup_code = State()

    registration_stamp = State()


async def sm_start(query: types.CallbackQuery, callback_data: dict):
    try:
        # remove callback button after click on it:
        await dp.bot.edit_message_text(text=TEXT_USER_NOT_FOUND_IN_DB, chat_id=query.from_user.id,
                                       message_id=query.message.message_id)

        user_id = query.from_user.id
        username = query.from_user.username

        # The user may already be in the database. Let's check it.
        try:
            is_user_registered = await postgre.is_user_registered(user_id)
            if is_user_registered:
                return

        except postgre.ps.OperationalError as error:
            logger.exception(f"POSTGRESQL: {error}")
        except (AttributeError, OSError) as error:
            logger.exception(error)

        logger.info(f"User @{username} [{user_id}] started the survey.")

        # save user_id to database:
        await FSMUserSurvey.user_id.set()
        save_state = dp.get_current().current_state()
        await save_state.update_data(user_id=user_id)

        await FSMUserSurvey.username.set()
        await dp.bot.send_message(chat_id=user_id, text="Как мне тебя называть\?")

    except (BadRequest, Unauthorized) as aiogram_error:
        if DEBUG_MODE:
            await dp.bot.send_message(chat_id=query.from_user.id,
                                      text=f"{aiogram_error}\n"
                                           f"Please contact the administrator: @RUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUR",
                                      parse_mode=types.ParseMode.HTML)
        logger.exception(aiogram_error)


async def sm_user_name(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        username_source = str(message.text)
        username = ""

        # Remove non alpha chars from username:
        for char in username_source:
            if char.isalpha() or char.isdigit():
                username += char

        async with state.proxy() as data:
            data["username"] = username
            
        await FSMUserSurvey.group_name.set()

        available_groups = await postgre.get_groups(convert_to_str=True)
        await dp.bot.send_message(chat_id=user_id, text=TEXT_SM_USER_GROUP_NAME)  # USER GROUP NAME
        await dp.bot.send_message(chat_id=user_id, text=f"Доступные группы: {available_groups}", parse_mode=types.ParseMode.HTML)

    except (BadRequest, Unauthorized) as aiogram_error:
        if DEBUG_MODE:
            await dp.bot.send_message(chat_id=message.from_user.id,
                                      text=f"{aiogram_error}\n"
                                           f"Please contact the administrator: @RUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUR",
                                      parse_mode=types.ParseMode.HTML)
        logger.exception(aiogram_error)


async def sm_group_name(message: types.Message, state: FSMContext):
    try:
        user_group = str(message.text).upper()
        available_groups_tuple = await postgre.get_groups(convert_to_str=False)

        if user_group.upper() in available_groups_tuple:
            async with state.proxy() as data:
                data["group_name"] = user_group

            await FSMUserSurvey.subgroup_code.set()
            await message.reply(TEXT_SM_USER_SUBGROUP_CODE, reply_markup=kb_survey_subgroup)
        else:
            group_not_found = "Группа не найдена в базе данных\!" \
                              "\nВыберите из списка доступных групп\." \
                              "\nВозможно, есть ошибка в вводе\." \
                              "\n\nПример ввода: \'is\-31\'"
            await message.reply(group_not_found)
    except (BadRequest, Unauthorized) as aiogram_error:
        if DEBUG_MODE:
            await dp.bot.send_message(chat_id=message.from_user.id,
                                      text=f"{aiogram_error}\n"
                                           f"Please contact the administrator: @RUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUR",
                                      parse_mode=types.ParseMode.HTML)
        logger.exception(aiogram_error)


async def sm_subgroup_code(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    user_id = query.from_user.id
    try:
        # remove keyboard after click on it
        await dp.bot.edit_message_text(text=query.message.text, chat_id=query.from_user.id,
                                       message_id=query.message.message_id)

        if callback_data['value']:
            async with state.proxy() as data:
                data["subgroup_code"] = callback_data['value']
        else:
            await dp.bot.send_message(chat_id=user_id, text="Некорректный ввод\!")

    except (BadRequest, Unauthorized) as aiogram_error:
        if DEBUG_MODE:
            await dp.bot.send_message(chat_id=user_id,
                                      text=f"{aiogram_error}\n"
                                           f"Please contact the administrator: @RUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUR",
                                      parse_mode=types.ParseMode.HTML)
        logger.exception(aiogram_error)

    try:
        user_data = await state.get_data()
        TEXT = f"Проверим: \n" \
               f"Тебя зовут {user_data['username']}.\n" \
               f"Учишься в группе {user_data['group_name']}, " \
               f"в подгруппе #{user_data['subgroup_code']}.\n"

        await dp.bot.send_message(chat_id=user_id, text=TEXT, parse_mode=types.ParseMode.HTML)

        await dp.bot.send_message(chat_id=user_id, text="Данные записаны верно\?", reply_markup=kb_survey_correct)

        await FSMUserSurvey.registration_stamp.set()

    except (BadRequest, Unauthorized) as aiogram_error:
        if DEBUG_MODE:
            await dp.bot.send_message(chat_id=query.from_user.id,
                                      text=f"{aiogram_error}\n"
                                           f"Please contact the administrator: @RUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUR",
                                      parse_mode=types.ParseMode.HTML)
        logger.exception(aiogram_error)

# async def sm_validate_user_info(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
#     try:
#         user_id = query.from_user.id
#         user_data = await state.get_data()
#         TEXT = f"Тебя зовут {user_data['username']}.\n" \
#                f"Учишься в группе {user_data['group_name']}, " \
#                f"в подгруппе #{user_data['subgroup_code']}.\n"
#
#         await dp.bot.send_message(chat_id=user_id, text=TEXT, parse_mode=types.ParseMode.HTML)
#
#         await dp.bot.send_message(chat_id=user_id, text="Данные записаны верно\?", reply_markup=kb_survey_correct)
#
#         await FSMUserSurvey.registration_stamp.set()
#
#     except (BadRequest, Unauthorized) as aiogram_error:
#         if DEBUG_MODE:
#             await dp.bot.send_message(chat_id=query.from_user.id,
#                                       text=f"{aiogram_error}\n"
#                                            f"Please contact the administrator: @RUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUR",
#                                       parse_mode=types.ParseMode.HTML)
#         logger.exception(aiogram_error)


async def sm_registration_stamp(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    try:
        # remove keyboard after click on it
        await dp.bot.edit_message_text(text=query.message.text, chat_id=query.from_user.id,
                                       message_id=query.message.message_id)

        if callback_data['value']:
            try:
                registration_stamp = datetime.now(pytz.timezone('Europe/Moscow')).isoformat()

                state_reg = dp.get_current().current_state()
                await state_reg.update_data(registration_stamp=registration_stamp)

                if not SAVE_TO_DB:
                    logger.warning(f"SAVE_TO_DB is True. The data will not be sent to DB!")
                    await dp.bot.send_message(chat_id=query.from_user.id, text=f"DEBUG_MODE is True\n"
                                                                               f"The data will not be sent!", parse_mode=types.ParseMode.HTML)
                else:
                    state_data = await state.get_data()
                    if await postgre.execute_write_query('users',
                                                         tuple(state_data.values()),
                                                         'user_id, username, group_name, subgroup_code, '
                                                         'registration_stamp'):
                        await dp.bot.send_message(chat_id=query.from_user.id, text=texts.TEXT_SM_WE_GOT_IT)
            except (BadRequest, Unauthorized) as aiogram_error:
                if DEBUG_MODE:
                    await dp.bot.send_message(chat_id=query.from_user.id,
                                              text=f"{aiogram_error}\n"
                                                   f"Please contact the administrator: @RUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUR",
                                              parse_mode=types.ParseMode.HTML)
                logger.exception(aiogram_error)
        else:
            await dp.bot.send_message(chat_id=query.from_user.id, text="DATA IS INVALID. RESTART...", parse_mode=types.ParseMode.HTML)
            await sm_restart_reg(query, state, callback_data)
        await state.finish()

    except (BadRequest, Unauthorized) as aiogram_error:
        if DEBUG_MODE:
            await dp.bot.send_message(chat_id=query.from_user.id,
                                      text=f"{aiogram_error}\n"
                                           f"Please contact the administrator: @RUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUR",
                                      parse_mode=types.ParseMode.HTML)
        logger.exception(aiogram_error)


async def sm_restart_reg(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await dp.bot.send_message(chat_id=query.from_user.id, text="Регистрация перезапускается..", parse_mode=types.ParseMode.HTML)
    await state.finish()
    await FSMUserSurvey.user_id.set()

    await sm_start(query, callback_data)


def register_handlers_sm_user(dp: Dispatcher):
    dp.register_callback_query_handler(sm_start, survey_cb.filter(field="StartUserSurvey"))
    dp.register_message_handler(sm_user_name, state=FSMUserSurvey.username)
    dp.register_message_handler(sm_group_name, state=FSMUserSurvey.group_name)
    dp.register_callback_query_handler(sm_subgroup_code, survey_cb.filter(field="UserSurveySubgroup"), state=FSMUserSurvey.subgroup_code)
    dp.register_callback_query_handler(sm_registration_stamp, survey_cb.filter(field="SurveyCorrect"), state=FSMUserSurvey.registration_stamp)
    dp.register_callback_query_handler(sm_restart_reg, survey_cb.filter(field="SurveyIncorrect"), state=FSMUserSurvey.registration_stamp)

    logger.debug("State machine registered!")