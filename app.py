import logging

from aiogram import executor

from data import config
from loader import dp, bot
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    logging.info("started up")
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)

    if not config.DEBUG_MODE:
        await bot.set_webhook(config.POSTGRES_URI)


async def on_shutdown(dispatcher):
    if not config.DEBUG_MODE:
        await bot.delete_webhook()

# import psycopg2 as ps
#
#
# database_connection = ps.connect(config.POSTGRES_URI, sslmode='require')
#
#
# def execute_read_query(query: str = None):
#     """
#     Executes the read request.
#
#     :param query: Request text
#     :return: list of tuples [(content_id, author_id, ***), (content_id, author_id, ***)]
#     """
#
#     connection = database_connection
#     cursor = None
#     try:
#         cursor = connection.cursor()
#         cursor.execute(query)
#         result = cursor.fetchall()
#
#         # logger.info(f'Read-request "{query}" completed successfully!')
#         # logger.debug(f"Total rows count = {cursor.rowcount}")
#
#         print(f'Read-request "{query}" completed successfully!')
#         print(f"Total rows count = {cursor.rowcount}")
#         return result
#
#     except (Exception, ps.OperationalError) as error:
#         # logger.error(error)
#         print(error)
#     finally:
#         if connection:
#             cursor.close()
#             connection.close()
#             # logger.info("[CLOSED] Connection to PostgreSQL is successfully closed!")
#             print("[CLOSED] Connection to PostgreSQL is successfully closed!")
#
#
# @dp.message_handler(commands=['get'], commands_prefix='!/')
# async def on_get_message():
#     data = execute_read_query("SELECT * FROM schedule WHERE group_code = 'IS_31_4';")
#     await message.answer(str(data))

if __name__ == "__main__":
    if config.DEBUG_MODE:
        executor.start_polling(dispatcher=dp, on_startup=on_startup)
    else:
        executor.start_webhook(dispatcher=dp,
                               webhook_path="",
                               on_startup=on_startup,
                               on_shutdown=on_shutdown,
                               skip_updates=True,
                               host="0.0.0.0",
                               port=int(5000)
                               )
