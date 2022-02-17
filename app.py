import logging
import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import HOOK_URL
import psycopg2 as ps

logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

database_connection = ps.connect(os.environ.get("DATABASE_URL"), sslmode='require')


def execute_read_query(query: str = None):
    """
    Executes the read request.

    :param query: Request text
    :return: list of tuples [(content_id, author_id, ***), (content_id, author_id, ***)]
    """

    connection = database_connection
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        # logger.info(f'Read-request "{query}" completed successfully!')
        # logger.debug(f"Total rows count = {cursor.rowcount}")

        print(f'Read-request "{query}" completed successfully!')
        print(f"Total rows count = {cursor.rowcount}")
        return result

    except (Exception, ps.OperationalError) as error:
        # logger.error(error)
        print(error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            # logger.info("[CLOSED] Connection to PostgreSQL is successfully closed!")
            print("[CLOSED] Connection to PostgreSQL is successfully closed!")


bot = Bot(token=os.environ.get("TG_TOKEN"))
dp = Dispatcher(bot)


async def on_startup(dp):
    await bot.set_webhook(HOOK_URL)


async def on_shutdown(dp):
    await bot.delete_webhook()
    database_connection.close()


@dp.message_handler(commands=['start'], commands_prefix='!/')
async def on_start_message(message: types.Message):
    await message.answer(f"I got ur /start message, {message.from_user.first_name}!")


@dp.message_handler(commands=['new'], commands_prefix='!/')
async def on_start_message(message: types.Message):
    await message.answer(f"I got ur /new message, {message.from_user.first_name}!")


@dp.message_handler(commands=['edit'], commands_prefix='!/')
async def on_start_message(message: types.Message):
    await message.answer(f"I got ur /edit message, {message.from_user.first_name}!")


@dp.message_handler(commands=['delete'], commands_prefix='!/')
async def on_start_message(message: types.Message):
    await message.answer(f"DON'T TOUCH IT! OK?")


@dp.message_handler(commands=['get'], commands_prefix='!/')
async def on_get_message(message: types.Message):
    await message.answer("Введи день недели (1-5): ")
    # answer = message.text

    data = execute_read_query("SELECT * FROM schedule WHERE group_code = 'IS_31_4';")

    await message.answer(str(data))


executor.start_webhook(dispatcher=dp,
                       webhook_path="",
                       on_startup=on_startup,
                       on_shutdown=on_shutdown,
                       skip_updates=True,
                       host="0.0.0.0",
                       port=int(os.environ.get("PORT", 5000))
                       )
