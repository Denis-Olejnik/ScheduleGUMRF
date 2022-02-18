from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from loguru import logger

from data import texts
from database import postgre
from handlers.user_survey import sm_start
from keyboards import user_inline_keyboard
from loader import dp


async def cmd_start(message: types.Message):
    await message.answer(text=texts.on_start_command, reply_markup=user_inline_keyboard)
    logger.info(f"User @{message.from_user.username} [{message.from_user.id}] start conversation with bot!")


async def show_schedule(message: types.Message):
    user_id = message.from_user.id
    user_has_registered = await postgre.has_user_registered(user_id)

    if not user_has_registered:
        # await sm_start()
        print('USER NOT FOUNDED IN DB')
    else:
        await message.answer("Отправляю расписание")


def register_handlers_base(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_callback_query_handler(show_schedule)
    logger.debug("Handler registered!")
