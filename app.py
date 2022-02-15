import os

from aiogram import Bot, types, utils
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InputTextMessageContent, input_message_content

from data.config import TG_TOKEN, HOOK_URL
import psycopg2 as ps

database = ps.connect(os.environ.get("DATABASE_URL"), sslmode='require')
curr = database.cursor()

bot = Bot(token=TG_TOKEN)
dispatcher = Dispatcher(bot)


async def on_startup(dispatcher):
    await bot.set_webhook(HOOK_URL)



async def on_shutdown(dispatcher, message: types.Message):
    await message.answer("shutdowned!")
    await bot.delete_webhook()
    curr.close()
    database.close()


@dispatcher.message_handler()
async def on_start_message(message: types.Message):
    await message.answer("Я получил твоё сообщение!")



executor.start_webhook(dispatcher=dispatcher,
                       webhook_path="",
                       on_startup=on_startup,
                       on_shutdown=on_shutdown,
                       skip_updates=True,
                       host="0.0.0.0",
                       port=int(os.environ.get("PORT", 5000))
                       )
