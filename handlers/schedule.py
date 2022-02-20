
from loader import dp

from aiogram import Dispatcher, types


async def show_schedule(callback: types.CallbackQuery = None, message: types.Message = None):
    user_id = callback.from_user.id
    await dp.bot.send_message(chat_id=user_id, text="GET USER SCHEDULE")

    # user_id = dp.bot.from_user.id
    # user_has_registered = await postgre.is_user_registered(user_id)
    #
    # if not user_has_registered:
    #     await sm_start(message)
    #     logger.warning(F"User {message.from_user.username} [{message.from_user.id}] not founded in DB!")
    # else:
    #     try:
    #         await message.answer("Получаю расписание")
    #         user_data = await postgre.execute_read_query(f"SELECT * FROM users WHERE user_id = {user_id}")
    #         user_data = user_data[0]
    #         user_group = f"{user_data[1]}_{user_data[2]}"
    #
    #         day_of_week = datetime.today().isocalendar()[2]
    #         current_week = datetime.today().isocalendar()[1]
    #         fractional = int(current_week) % 2  # Расчёт числителя или знаменателя
    #
    #         # TODO: Выделять текущую пару относительно времени (9.30 < x < 11.15)
    #
    #         if DEBUG_MODE:
    #             week_day = random.choice([1, 2, 3, 4])
    #             fractional = random.choice([0, 1])
    #             user_group = "IS_31_" + str(random.randrange(1, 3))
    #             print(f"group={user_group}, fractional={fractional}, day of the week = {week_day}")
    #
    #             schedule = await postgre.get_user_schedule_for_day(user_group, week_day, fractional)
    #             schedule = schedule[0][0]
    #
    #             schedule = f"\nГруппа: {user_group}, День недели: {week_day}, Дробь: {fractional}\n\n" + schedule
    #
    #             await dp.bot.send_message(chat_id=user_id, text=schedule)
    #
    #     except (Exception) as err:
    #         logger.exception(err)

#
# def register_callback_query_handler(dp: Dispatcher):
#     dp.register_callback_query_handler(show_schedule, text="show_user_schedule")
