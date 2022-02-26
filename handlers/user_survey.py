from datetime import datetime
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.utils.exceptions import Unauthorized, BadRequest
from loguru import logger

from data import TEXT_SM_WELCOME_MSG, TEXT_SM_USER_GROUP_NAME, TEXT_SM_USER_SUBGROUP_CODE, texts
from data.config import DEBUG_MODE, DONT_SAVE_TO_DB
from database import postgre

from keyboards.survey_keyboard import survey_cb, kb_survey_correct
from loader import dp


class FSMUserSurvey(StatesGroup):
    user_id = State()

    username = State()
    group_name = State()
    subgroup_code = State()
    reminder_time = State()

    registration_stamp = State()


async def sm_start(query: types.CallbackQuery, callback_data: dict):
    try:
        # remove callback button after click on it:
        await dp.bot.edit_message_text(text=query.message.text, chat_id=query.from_user.id,
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

        await dp.bot.send_message(chat_id=user_id, text=TEXT_SM_WELCOME_MSG)  # SURVEY STARTED...

        # save user_id to database:
        await FSMUserSurvey.user_id.set()
        save_state = dp.get_current().current_state()
        await save_state.update_data(user_id=user_id)

        await FSMUserSurvey.username.set()
        await dp.bot.send_message(chat_id=user_id, text="Привет\! Как тебя зовут\?")

    except (BadRequest, Unauthorized) as aiogram_error:
        if DEBUG_MODE:
            await dp.bot.send_message(chat_id=query.from_user.id,
                                      text=f"{aiogram_error}\n"
                                           f"Please contact the administrator: @RUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUR")
        logger.exception(aiogram_error)


async def sm_user_name(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        username = str(message.text)

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
                                           f"Please contact the administrator: @RUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUR")
        logger.exception(aiogram_error)


async def sm_group_name(message: types.Message, state: FSMContext):
    try:
        user_group = str(message.text).upper()
        available_groups_tuple = await postgre.get_groups(convert_to_str=False)

        if user_group.upper() in available_groups_tuple:
            async with state.proxy() as data:
                data["group_name"] = user_group

            await FSMUserSurvey.subgroup_code.set()
            await message.reply(TEXT_SM_USER_SUBGROUP_CODE)
        else:
            await message.reply("Группа не найдена в базе данных\! Выберите из списка доступных групп.")

    except (BadRequest, Unauthorized) as aiogram_error:
        if DEBUG_MODE:
            await dp.bot.send_message(chat_id=message.from_user.id,
                                      text=f"{aiogram_error}\n"
                                           f"Please contact the administrator: @RUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUR")
        logger.exception(aiogram_error)


async def sm_subgroup_code(message: types.message, state: FSMContext):
    try:
        if str(message.text) in ['1', '2']:
            async with state.proxy() as data:
                data["subgroup_code"] = str(message.text)

            await dp.bot.send_message(chat_id=message.from_user.id, text="Пожалуйста, укажите за сколько минут до начала пары отравлять уведомление:")
            await FSMUserSurvey.reminder_time.set()

        else:
            await message.reply("Введите корректный код подгруппы\!")

    except (BadRequest, Unauthorized) as aiogram_error:
        if DEBUG_MODE:
            await dp.bot.send_message(chat_id=message.from_user.id,
                                      text=f"{aiogram_error}\n"
                                           f"Please contact the administrator: @RUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUR")
        logger.exception(aiogram_error)


async def sm_reminder_time(message: types.message, state:FSMContext):
    try:
        async with state.proxy() as data:
            data["reminder_time"] = str(message.text)

        user_data = await state.get_data()
        TEXT = f"user_id: {user_data['user_id']}\n\n" \
               f"username: {user_data['username']}\n" \
               f"group_name: {user_data['group_name']}\n" \
               f"subgroup_code: {user_data['subgroup_code']}\n" \
               f"reminder_time: {user_data['reminder_time']}"
        await message.answer(TEXT, parse_mode=types.ParseMode.HTML)

        await message.answer("Данные записаны верно\?", reply_markup=kb_survey_correct)

        await FSMUserSurvey.registration_stamp.set()

    except (BadRequest, Unauthorized) as aiogram_error:
        if DEBUG_MODE:
            await dp.bot.send_message(chat_id=message.from_user.id,
                                      text=f"{aiogram_error}\n"
                                           f"Please contact the administrator: @RUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUR")
        logger.exception(aiogram_error)


async def sm_registration_stamp(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    try:
        # remove keyboard after click on it
        await dp.bot.edit_message_text(text=query.message.text, chat_id=query.from_user.id,
                                       message_id=query.message.message_id)

        if callback_data['value']:

            registration_stamp = datetime.now().isoformat()

            state_reg = dp.get_current().current_state()
            await state_reg.update_data(registration_stamp=registration_stamp)

            if DONT_SAVE_TO_DB:
                logger.warning(f"DEBUG_MODE is {DEBUG_MODE}. The data will not be sent!")
                await dp.bot.send_message(chat_id=query.from_user.id, text=f"DEBUG_MODE is {DEBUG_MODE}. "
                                                                           f"The data will not be sent\!")
            else:
                state_data = await state.get_data()
                if await postgre.execute_write_query('users',
                                                     tuple(state_data.values()),
                                                     'user_id, username, group_name, subgroup_code, '
                                                     'reminder_time, registration_stamp'):
                    await dp.bot.send_message(chat_id=query.from_user.id, text=texts.TEXT_SM_WE_GOT_IT)
        else:
            await dp.bot.send_message(chat_id=query.from_user.id, text="DATA IS INVALID. RESTART...")
        await state.finish()

    except (BadRequest, Unauthorized) as aiogram_error:
        if DEBUG_MODE:
            await dp.bot.send_message(chat_id=query.from_user.id,
                                      text=f"{aiogram_error}\n"
                                           f"Please contact the administrator: @RUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUR")
        logger.exception(aiogram_error)


async def sm_restart_reg(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await dp.bot.send_message(chat_id=query.from_user.id, text="Регистрация перезапускается..", parse_mode=types.ParseMode.HTML )
    await state.finish()
    await FSMUserSurvey.user_id.set()

    await sm_start(query, callback_data)


def register_handlers_sm_user(dp: Dispatcher):
    dp.register_callback_query_handler(sm_start, survey_cb.filter(field="StartUserSurvey"))
    dp.register_message_handler(sm_user_name, state=FSMUserSurvey.username)
    dp.register_message_handler(sm_group_name, state=FSMUserSurvey.group_name)
    dp.register_message_handler(sm_subgroup_code, state=FSMUserSurvey.subgroup_code)
    dp.register_message_handler(sm_reminder_time, state=FSMUserSurvey.reminder_time)
    dp.register_callback_query_handler(sm_registration_stamp, survey_cb.filter(field="SurveyCorrect"), state=FSMUserSurvey.registration_stamp)
    dp.register_callback_query_handler(sm_restart_reg, survey_cb.filter(field="SurveyIncorrect"), state=FSMUserSurvey.registration_stamp)

    logger.debug("State machine registered!")