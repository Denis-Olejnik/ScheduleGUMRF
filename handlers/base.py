from aiogram import Dispatcher, types
from loguru import logger
from keyboards import user_markup_keyboard, user_inline_keyboard
from data import texts


async def cmd_start(message: types.Message):
    await message.answer(text=texts.on_start_command, reply_markup=user_inline_keyboard)
    logger.info(f"User @{message.from_user.username} [{message.from_user.id}] start conversation with bot!")


def register_handlers_base(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'])
    logger.debug("Handler registered!")
