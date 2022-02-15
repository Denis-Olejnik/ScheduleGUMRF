import logging
import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import HOOK_URL
import psycopg2 as ps

logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

database = ps.connect(os.environ.get("DATABASE_URL"), sslmode='require')
curr = database.cursor()

bot = Bot(token=os.environ.get("TG_TOKEN"))
dp = Dispatcher(bot)


async def on_startup(dp):
    await bot.set_webhook(HOOK_URL)


async def on_shutdown(dp):
    await bot.delete_webhook()
    curr.close()
    database.close()


@dp.message_handler(commands=['start'], commands_prefix='!/')
async def on_start_message(message: types.Message):
    await message.answer(f"I got ur /start message,{message.from_user.first_name}!")


@dp.message_handler(commands=['new'], commands_prefix='!/')
async def on_start_message(message: types.Message):
    await message.answer(f"I got ur /new message,{message.from_user.first_name}!")


@dp.message_handler(commands=['edit'], commands_prefix='!/')
async def on_start_message(message: types.Message):
    await message.answer(f"I got ur /edit message,{message.from_user.first_name}!")


@dp.message_handler(commands=['delete'], commands_prefix='!/')
async def on_start_message(message: types.Message):
    await message.answer(f"DON'T TOUCH IT! OK?")


executor.start_webhook(dispatcher=dp,
                       webhook_path="",
                       on_startup=on_startup,
                       on_shutdown=on_shutdown,
                       skip_updates=True,
                       host="0.0.0.0",
                       port=int(os.environ.get("PORT", 5000))
                       )
