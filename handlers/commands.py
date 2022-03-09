from aiogram import Dispatcher, types
from aiogram.utils.exceptions import BadRequest, Unauthorized
from loguru import logger

from data import texts, config
from data.texts import TEXT_USER_NOT_FOUND_IN_DB, TEXT_IN_DEV_MODE, TEXT_USER_MENU
from database import postgre
from keyboards import kb_start_user_survey, USER_MENU
from keyboards.menu.admin_keyboard import ADMIN_MENU
from loader import dp


async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    try:
        if str(user_id) not in config.TELEGRAM_ALLOWED_USERS and config.TELEGRAM_ONLY_ALLOWED:
            await message.reply(text=TEXT_IN_DEV_MODE + f"ID: {user_id}")
            logger.info(f"User {user_id} is not allowed.")

            return
    except (BadRequest, Unauthorized) as aiogram_error:
        await dp.bot.send_message(chat_id=user_id, text=aiogram_error, parse_mode=types.ParseMode.HTML)
        logger.exception(aiogram_error)

    logger.info(f"User @{message.from_user.username} [{message.from_user.id}] start conversation with bot!")

    is_user_registered = await postgre.is_user_registered(message.from_user.id)
    if is_user_registered:
        await dp.bot.send_message(chat_id=user_id, text=TEXT_USER_MENU, reply_markup=USER_MENU)
    else:
        await message.answer(text=texts.TEXT_ON_START_COMMAND, reply_markup=types.ReplyKeyboardRemove())
        await dp.bot.send_message(chat_id=message.from_user.id,
                                  text=TEXT_USER_NOT_FOUND_IN_DB,
                                  reply_markup=kb_start_user_survey)


async def cmd_admin(message: types.Message):
    user_id = message.from_user.id
    try:
        if str(user_id) in config.TELEGRAM_ADMINS:
            await dp.bot.send_message(chat_id=user_id, text='Меню администратора', reply_markup=ADMIN_MENU)
    except (BadRequest, Unauthorized) as aiogram_error:
        await dp.bot.send_message(chat_id=user_id, text=aiogram_error, parse_mode=types.ParseMode.HTML)
        logger.exception(aiogram_error)


def register_handlers_base(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(cmd_admin, commands=['admin'])
    logger.debug("Commands handler registered!")
