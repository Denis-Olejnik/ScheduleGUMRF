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

	dt = datetime.datetime.now().replace(hour=int(list_of_time[0][0:2]),minute=int(list_of_time[0][3:5]))
	dt_now = datetime.datetime.now()

	time_interval = dt - dt_now
	converter = time_interval.total_seconds()
	
	# print("Время до пары:",converter)
	# print("Время до напоминания", int(converter)-600)

	# time.sleep(int(converter)-600)

	# print("Para scoro")


