from datetime import datetime, date

from aiogram import Dispatcher, types
from loguru import logger

from data import texts, config
from data.texts import TEXT_USER_NOT_FOUND_IN_DB
from database import postgre
from handlers.schedule_sender import show_schedule
from keyboards import kb_start_user_survey
from loader import dp


async def cmd_start(message: types.Message):
    user_id = message.from_user.id

    if str(user_id) not in config.TELEGRAM_ALLOWED_USERS and config.TELEGRAM_ONLY_ALLOWED:
        BOT_IN_DEV_TEXT = f"BOT is in development mode. \nYour uid \({user_id}\) is not found in the allowed list. \n" \
                          f"Please contact admin to add it: @RUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUR"
        await message.reply(BOT_IN_DEV_TEXT)
        return

    logger.info(f"User @{message.from_user.username} [{message.from_user.id}] start conversation with bot!")

    is_user_registered = await postgre.is_user_registered(message.from_user.id)
    if is_user_registered:
        await show_schedule(message)
    else:
        await message.answer(text=texts.TEXT_ON_START_COMMAND)
        await dp.bot.send_message(chat_id=message.from_user.id, text=TEXT_USER_NOT_FOUND_IN_DB,
                                  reply_markup=kb_start_user_survey)


def register_handlers_base(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'])
    logger.debug("Commands handler registered!")
