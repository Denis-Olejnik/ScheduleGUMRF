from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.utils.exceptions import Unauthorized, BadRequest
from loguru import logger

from transliterate import translit
import re

from data import TEXT_SM_WELCOME_MSG, TEXT_SM_USER_GROUP_NAME
from database import postgre

from keyboards.survey_keyboard import survey_cb, kb_survey_group
from loader import dp


class FSMUserSurvey(StatesGroup):
    user_id = State()
    group_name = State()
    subgroup_code = State()

    registration_stamp = State()


async def sm_start(query: types.CallbackQuery):
    try:
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

        await dp.bot.send_message(chat_id=user_id, text=TEXT_SM_WELCOME_MSG)

        
        # # Get user_id and write it state:
        # await FSMUserSurvey.user_id.set()
        # write_id_state = dp.get_current().current_state()
        # await write_id_state.update_data(user_id=user_id)
        #
        # # Set state to record a user group:
        # await FSMUserSurvey.group_name.set()

        await dp.bot.send_message(chat_id=user_id, text=TEXT_SM_USER_GROUP_NAME, reply_markup=kb_survey_group)

    except (BadRequest, Unauthorized) as aiogram_error:
        logger.exception(aiogram_error)

#
# async def cancel_user_survey(message: types.Message, state: FSMContext):
#     current_state = await state.get_state()
#     if current_state is None:
#         return
#     await state.finish()
#     await message.reply('Опрос отменён.')
#


async def sm_group_name(query: types.CallbackQuery, callback_data: dict):
    await dp.bot.send_message(chat_id=query.from_user.id, text=f"{callback_data}")
    # try:
    #     user_id = query.from_user.id
    #     logger.info(callback_data)
    # # async with state.proxy() as data:
    # #     group_name = message.text.upper()
    # #     group_name = re.sub('[!@#$%&*()\\-+ \'\"]', '_', group_name)  # replace chars to '_'
    # #
    # #     group_name = translit(group_name, "ru", reversed=True)
    # #     data['group_name'] = group_name
    # #
    # # await FSMUserSurvey.next()
    # #
    # # await message.reply(texts.TEXT_SM_USER_SUBGROUP_CODE, reply_markup=keyboard_subgroup_code)
    #     await dp.bot.send_message(chat_id=query.from_user.id, text="subgroup", reply_markup=kb_survey_subgroup)
    #
    # except Exception:
    #     logger.error('12')


# Get user subgroup code:
# async def sm_subgroup_code(query: types.CallbackQuery, callback_data: dict):
#     logger.info("WRITE subgroup_code")
#     # async with state.proxy() as data:
#     #     data['subgroup_code'] = int(message.text)
#
#     # await FSMUserSurvey.next()
#
#     # await message.reply(texts.TEXT_SM_USER_IS_LEADER, reply_markup=keyboard_group_leader)
#     await dp.bot.send_message(chat_id=query.from_user.id, text="check", reply_markup=kb_survey_correct)

# async def sm_subgroup_code(call: types.ChatType, state: FSMContext):
#     async with state.proxy() as data:
#         if call == "subgroup_1":
#             data['subgroup_code'] = 1
#         elif call == "subgroup_2":
#             data['subgroup_code'] = 2
#
#     await FSMUserSurvey.next()
#
#     await dp.bot.send_message(texts.TEXT_SM_USER_IS_LEADER, reply_markup=keyboard_group_leader)


# Get user status in group:
# async def sm_is_leader(message: types.Message, state: FSMContext):
    # async with state.proxy() as data:
    #     data['is_leader'] = str(message.text)
    #
    # await FSMUserSurvey.next()

    # data_parsed = f"Группа: {data['group_name']}\n" \
    #               f"Подгруппа: {data['subgroup_code']}\n" \
    #
    # message_check = f"{texts.TEXT_SM_DATA_VALIDATION}\n{data_parsed}"
    # await dp.bot.send_message(message.from_user.id, message_check, reply_markup=keyboard_results)


# Validate typed data:
# async def sm_set_registration_stamp(message: types.Message, state: FSMContext):
#     pass
#     # if message.text == "Да":
#     #     async with state.proxy() as data:
#     #         timestamp = datetime.datetime.now().isoformat()
#     #         data['registration_stamp'] = timestamp
#     #
#     #     if DEBUG_MODE:
#     #         logger.warning(f"DEBUG_MODE is {DEBUG_MODE}. The data will not be sent!")
#     #         await message.reply(f"DEBUG_MODE is {DEBUG_MODE}. The data will not be sent!")
#     #
#     #     else:
#     #         await postgre.execute_write_query('users', tuple(data.values()),
#     #                                           'user_id, group_name, subgroup_code, registration_stamp')
#     #
#     #         await message.reply(texts.TEXT_SM_WE_GOT_IT)
#     #
#     #     data_parsed = f"group_name: {data['group_name']}, subgroup_code: {data['subgroup_code']}"
#     #
#     #     logger.info(f"User {message.from_user.id} (@{message.from_user.username}) "
#     #                 f"uploaded the following information: {data_parsed}")
#     #
#     #     await state.finish()
#     # else:
#     #     await message.reply("Заполняем заново...")


def register_handlers_sm_user(dp: Dispatcher):
    dp.register_callback_query_handler(sm_start, survey_cb.filter(field="StartUserSurvey"), state=None)
    dp.register_callback_query_handler(sm_group_name, survey_cb.filter(field="SurveyGroupName"), state=None)
    # dp.register_callback_query_handler(sm_subgroup_code, survey_cb.filter(field="UserSurveySubgroup"), state=None)

    # dp.register_message_handler(cancel_user_survey, state="*", commands='cancel_survey')
    # dp.register_message_handler(cancel_user_survey, Text(equals='cancel_survey', ignore_case=True), state="*")

    # dp.register_message_handler(sm_set_registration_stamp, state=FSMUserSurvey.registration_stamp)

    logger.debug("State machine registered!")


# TODO: Добавить клавиатуру для выбора варианта ответа (Подгруппа: 1 / 2)
#  TOOD: Проверять корректность названия группы
#  TODO: Сделать запись в БД
#  TODO: Если что-то заполнено неправильно, то следует дать возможность исправить (или начать сначала)
#  TODO: Отлавливать сторонние команды ('/start')
