import datetime
import makara
import time

weekdays = {1:"Понедельник",2:"Вторник",3:"Среда",4:"Четверг",5:"Пятница",6:"Суббота",7:"Воскресенье"}
fraction = {1:"Числитель",0:"Знаменатель"}
list_of_time = ["19:20"]

def main():

	total_info = {} # Словарь для конечного вывода
	list_of_lessons = [] # Список для вывода пар

	day = datetime.datetime.today().isocalendar()[2]
	week = datetime.datetime.today().isocalendar()[1]

	calc = int(week) % 2 #Расчёт числителя или знаменателя
	# Обработка для Числителя
	if calc == 1: 
		handler = makara.numerator[day-1]
		for i in range(0,len(makara.numerator[day-1])):
			list_of_lessons.append(handler[i])
	# Обработка для Знаменателя
	elif calc == 0:
		handler = makara.denominator[day-1]
		for i in range(0,len(makara.denominator[day-1])):
			list_of_lessons.append(handler[i])

	total_info["Fraction"] = fraction[calc]
	total_info["Count_of_week"] = week
	total_info["Weekday"] = weekdays[day]
	total_info["lessons"] = list_of_lessons

	print(total_info)

def timer():

	for i in range(0,len(list_of_time)):
		dt = datetime.datetime.now().replace(hour=int(list_of_time[i][0:2]),minute=int(list_of_time[i][3:5]))
		dt_now = datetime.datetime.now()

		# print(str(dt_now.hour)+":"+str(dt_now.minute))
		# print(str(dt.hour)+":"+str(dt.minute))

		time_interval = dt - dt_now
		converter = time_interval.total_seconds()

		# print("Время до пары:",converter)
		# print("Время до напоминания:", int(converter)-600)

		# time.sleep(int(converter)-600)
		
def user_timer():
	dt_user = datetime.datetime.now().replace(hour=int(user_time[0:2]),minute=int(user_time[3:5]))
	dt_now_user = datetime.datetime.now()
	time_interval_user = dt_user - dt_now_user
	converter_user = time_interval_user.total_seconds()
	# print("Текущее время:",dt_now_user.strftime("%H:%M"))
	# print("Ожидание:",int(converter_user),"секунд")
	time.sleep(int(converter_user))
	# print("Время ожидания окончено")

