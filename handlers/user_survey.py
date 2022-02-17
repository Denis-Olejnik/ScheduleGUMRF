from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from loguru import logger


from data import texts
from loader import dp


class FSMUserSurvey(StatesGroup):
    user_group_code = State()  # Which group does the user belong to?
    user_subgroup_code = State()  # Which subgroup?
    user_group_leader = State()  # Is the user a group leader?
    all_correct = State()  # Everything is correct


async def sm_start(message: types.Message):
    user_id = message.from_user.id

    await dp.bot.send_message(user_id, texts.sm_welcome_message)
    await FSMUserSurvey.user_group_code.set()

    await message.reply(texts.sm_user_group_code)


async def sm_group_code(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['user_group_code'] = message.text

    await FSMUserSurvey.next()

    await message.reply(texts.sm_user_subgroup_code)


async def sm_subgroup_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_subgroup_code'] = message.text

    await FSMUserSurvey.next()

    await message.reply(texts.sm_user_group_leader)


async def sm_user_is_leader(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['user_group_leader'] = message.text

    await FSMUserSurvey.next()

    # await message.reply(texts.sm_everything_is_correct)
    data_parsed = f"Группа: {data['user_group_code']}\n" \
                  f"Подгруппа: {data['user_subgroup_code']}\n" \
                  f"Являешься старостой: {data['user_group_leader']}"

    message_check = f"{texts.sm_everything_is_correct}\n{data_parsed}"

    await dp.bot.send_message(message.from_user.id, message_check)


async def sm_everything_is_correct(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['all_correct'] = message.text

    if message.text == "Да":
        await message.reply(texts.sm_we_got_it)

        async with state.proxy() as data:
            # TODO: database saver here.
            pass

        data_parsed = f"Group: {data['user_group_code']}, subgroup: {data['user_subgroup_code']}, " \
                      f"leader: {data['user_group_leader']}"

        logger.warning(f'User {message.from_user.id} (@{message.from_user.username}) '
                       f'uploaded the following information: {data_parsed}')

        await state.finish()
    else:
        await message.reply("Заполняем заново...")


@dp.message_handler(state="*", commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state="*")
async def cancel_user_survey(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Done')


def register_handlers_sm_user(dp: Dispatcher):
    dp.register_message_handler(sm_start, commands=['survey'], state=None)

    dp.register_message_handler(cancel_user_survey, state="*", commands='cancel')
    dp.register_message_handler(cancel_user_survey, Text(equals='cancel', ignore_case=True), state="*")

    dp.register_message_handler(sm_group_code, state=FSMUserSurvey.user_group_code)
    dp.register_message_handler(sm_subgroup_code, state=FSMUserSurvey.user_subgroup_code)
    dp.register_message_handler(sm_user_is_leader, state=FSMUserSurvey.user_group_leader)
    dp.register_message_handler(sm_everything_is_correct, state=FSMUserSurvey.all_correct)

    logger.debug("State machine registered!")


# TODO: Добавить клавиатуру для выбора варианта ответа (Подгруппа: 1 / 2)
#  TOOD: Проверять корректность названия группы
#  TODO: Сделать запись в БД
#  TODO: Если что-то заполнено неправильно, то следует дать возможность исправить (или начать сначала)

