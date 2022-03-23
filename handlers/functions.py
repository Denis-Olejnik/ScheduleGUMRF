from database import postgre

from datetime import datetime,timedelta
import time

import schedule

# TODO:
# ДАТЬ ВОЗМОЖНОСТЬ ЮЗЕРАМ ВЫБИРАТЬ ДЕНЬ(СЕГОДНЯ/ЗАВТРА)

weekdays = {1:"Понедельник",2:"Вторник",3:"Среда",4:"Четверг",5:"Пятница",6:"Суббота",7:"Воскресенье"}
fraction = {1:"Числитель",0:"Знаменатель"}

lect_time = ["09:20","11:05","13:25","15:20"]
lect_time = ['14:22', '14:22', '14:22', '14:22']

connect = postgre.create_connection()

# Функция для получения задержки
def deley():

	# Глобальные переменые
	global group, subgroup, group_code
	global student_name
	global global_delay,global_time
	global day, week

	# Значение дня и недели(поделенное на 2 для Числителя и знаменателя)
	day = datetime.today().isocalendar()[2]
	week = datetime.today().isocalendar()[1] % 2

	# Листы для времени(лесс - чекает времена, которые ниже текущего)
	list_time = list()
	list_time_less = list()

	# Получение времени в юзерах
	users_time = postgre.execute_read_query(f"SELECT send_time FROM user_for_test WHERE spam_func = 'true'")

	# Текущее время и в стампе
	time_now = datetime.now()
	time_now_stamp = time_now.timestamp()

	# Цикл, который заменяет сегодняшнее время на время с send_time
	for i in range(0,len(users_time)):
		dt = datetime.now().replace(hour = int(users_time[i][0][0:2]),minute = int(users_time[i][0][3:5]))
		list_time.append(int(dt.timestamp()))

	# Цикл добавляет в лесс времена, которые ниже времени запсука программы
	for j in list_time:
		if j < time_now_stamp:
			list_time_less.append(j)

	# Ремувит из основного списка список лесса
	else: 
		for j in list_time_less:
			if j in list_time:
				list_time.remove(j)

	# Замена всех времен, которые ниже запуска, на некст день
	if list_time_less:
		delta = timedelta(days = 1)
		for k in range(len(list_time_less)):
			plus = int(datetime.timestamp(datetime.fromtimestamp(list_time_less[k]) + delta))
			list_time.append(plus)

	list_time.sort()
	
	# Берёт первое время из списка стамп времён
	test_time = datetime.fromtimestamp(list_time[0])

	# Обычное время(часы минуты для выборки из БД)
	take_time = str(datetime.fromtimestamp(list_time[0]).time())

	# перевод времени для БД
	global_time = take_time[0:2] + ":" + take_time[3:5]

	# Вычисление промежутка между временами и вывод в unix time
	global_delay = int((test_time - time_now).total_seconds())

	#Запрос в бд на основе сгенерированного времени
	request = postgre.execute_read_query(f"SELECT * from user_for_test WHERE send_time = '{global_time}'")
	
	student_name = request[0][1]
	group_code = str(request[0][2]) + "_" + str(request[0][3])

	print(global_delay)

# Функция для отправки сообщения
def sender():

	print(f"{student_name}, Вот твоё расписание на сегодня({weekdays[day]}[{fraction[week]}]):")

	schedule_now = postgre.execute_read_query(f"SELECT schedule_{week} FROM schedule WHERE group_code = '{group_code}' AND week_day = '{day}'")

	try:
		schedule_list = schedule_now[0][0]
		print(schedule_list)
	except Exception:
		pass

def sender_ten(x):

	# Получаем лист из группы, если включена функция
	list_boolean = postgre.execute_read_query(f"SELECT group_name, subgroup_code FROM user_for_test WHERE ten_before = 'true'")
	for i in range(0,len(list_boolean)):

		# Преобразуем group_name и subgroup_code в полноценную группу
		group_code_ten = str(list_boolean[i][0]) + "_" + str(list_boolean[i][1])

		# Получаем числитель или знаменатель
		
		req = postgre.execute_read_query(f"SELECT schedule_{week} FROM schedule WHERE group_code = '{group_code_ten}' AND week_day = '{day}'")

		# Получаем количество пар
		req = req[0][0].replace(",","").replace("\n",",").split(",")
		req_len = len(req)
		# Пробуем отправить по одной паре(сделано для того, чтобы таски не ломались, + чтобы не отслеживать количество пар, хотя функция есть)
		try:
			if req[x] != "Нет пары":
				print(req[x])
			else:
				continue
		except Exception:
			pass


# Запускаем первый раз для получения глобальной переменной
deley()

schedule.every(global_delay).seconds.do(sender)
schedule.every(global_delay).seconds.do(deley)

# По одной паре в определенное время
schedule.every().day.at(lect_time[0]).do(sender_ten,0)
schedule.every().day.at(lect_time[1]).do(sender_ten,1)
schedule.every().day.at(lect_time[2]).do(sender_ten,2)
schedule.every().day.at(lect_time[3]).do(sender_ten,3)


while True:
	schedule.run_pending()
	time.sleep(1)