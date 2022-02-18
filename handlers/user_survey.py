import datetime

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from loguru import logger

from transliterate import translit
import re
from data import texts
from data.config import DEBUG_MODE
from database import postgre
from keyboards import keyboard_subgroup_code, keyboard_group_leader, keyboard_results
from loader import dp


class FSMUserSurvey(StatesGroup):
    user_id = State()

    group_name = State()  # Which group does the user belong to?
    subgroup_code = State()  # Which subgroup?
    is_leader = State()  # Is the user a group leader?

    registration_stamp = State()


async def sm_start(message: types.Message):
    user_id = message.from_user.id
    user_has_registered = await postgre.has_user_registered(user_id)

    if user_has_registered:
        await message.reply("Похоже, что Вы уже проходили опрос.")
        logger.info(f"User @{message.from_user.username} [{message.from_user.id}] tried to start a survey!")
        return

    logger.info(f"User @{message.from_user.username} [{message.from_user.id}] started the survey.")

    await dp.bot.send_message(user_id, texts.sm_welcome_message)

    # get data and write it to state:
    await FSMUserSurvey.user_id.set()
    write_id_state = dp.get_current().current_state()
    await write_id_state.update_data(user_id=user_id)

    await FSMUserSurvey.group_name.set()

    await message.reply(texts.sm_user_group_code)


async def cancel_user_survey(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Опрос отменён.')


# Get user group name:
async def sm_group_name(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        group_name = message.text.upper()
        group_name = re.sub('[!@#$%&*()\\-+ \'\"]', '_', group_name)  # replace chars to '_'

        group_name = translit(group_name, "ru", reversed=True)
        data['group_name'] = group_name

    await FSMUserSurvey.next()

    await message.reply(texts.sm_user_subgroup_code, reply_markup=keyboard_subgroup_code)


# Get user subgroup code:
async def sm_subgroup_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['subgroup_code'] = int(message.text)

    await FSMUserSurvey.next()

    await message.reply(texts.sm_user_group_leader, reply_markup=keyboard_group_leader)

# async def sm_subgroup_code(call: types.ChatType, state: FSMContext):
#     async with state.proxy() as data:
#         if call == "subgroup_1":
#             data['subgroup_code'] = 1
#         elif call == "subgroup_2":
#             data['subgroup_code'] = 2
#
#     await FSMUserSurvey.next()
#
#     await dp.bot.send_message(texts.sm_user_group_leader, reply_markup=keyboard_group_leader)


# Get user status in group:
async def sm_is_leader(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['is_leader'] = str(message.text)

    await FSMUserSurvey.next()

    data_parsed = f"Группа: {data['group_name']}\n" \
                  f"Подгруппа: {data['subgroup_code']}\n" \
                  f"Являешься старостой: {data['is_leader']}\n" \

    message_check = f"{texts.sm_everything_is_correct}\n{data_parsed}"
    await dp.bot.send_message(message.from_user.id, message_check, reply_markup=keyboard_results)


# Validate typed data:
async def sm_set_registration_stamp(message: types.Message, state: FSMContext):
    if message.text == "Да":
        async with state.proxy() as data:
            timestamp = datetime.datetime.now().isoformat()
            data['registration_stamp'] = timestamp

        if DEBUG_MODE:
            logger.warning(f"DEBUG_MODE is {DEBUG_MODE}. The data will not be sent!")
            await message.reply(f"DEBUG_MODE is {DEBUG_MODE}. The data will not be sent!")

        else:
            await postgre.execute_write_query('users', tuple(data.values()),
                                              'user_id, group_name, subgroup_code, is_leader, registration_stamp')

            await message.reply(texts.sm_we_got_it)

        data_parsed = f"group_name: {data['group_name']}, subgroup_code: {data['subgroup_code']}, " \
                      f"is_leader: {data['is_leader']}"

        logger.info(f"User {message.from_user.id} (@{message.from_user.username}) "
                    f"uploaded the following information: {data_parsed}")

        await state.finish()
    else:
        await message.reply("Заполняем заново...")


def register_handlers_sm_user(dp: Dispatcher):
    dp.register_message_handler(sm_start, commands=['survey'], state=None)

    dp.register_message_handler(cancel_user_survey, state="*", commands='cancel_survey')
    dp.register_message_handler(cancel_user_survey, Text(equals='cancel_survey', ignore_case=True), state="*")

    dp.register_message_handler(sm_group_name, state=FSMUserSurvey.group_name)
    dp.register_message_handler(sm_subgroup_code, state=FSMUserSurvey.subgroup_code)
    dp.register_message_handler(sm_is_leader, state=FSMUserSurvey.is_leader)
    dp.register_message_handler(sm_set_registration_stamp, state=FSMUserSurvey.registration_stamp)

    logger.debug("State machine registered!")


# TODO: Добавить клавиатуру для выбора варианта ответа (Подгруппа: 1 / 2)
#  TOOD: Проверять корректность названия группы
#  TODO: Сделать запись в БД
#  TODO: Если что-то заполнено неправильно, то следует дать возможность исправить (или начать сначала)

