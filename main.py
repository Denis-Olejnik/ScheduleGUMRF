import datetime
import makara

weekdays = {1:"Понедельник",2:"Вторник",3:"Среда",4:"Четверг",5:"Пятница",6:"Суббота",7:"Воскресенье"}
fraction = {1:"Числитель",0:"Знаменатель"}

total_info = {}
list_of_lessons = []
c = 1

day = datetime.datetime.today().isocalendar()[2]
week = datetime.datetime.today().isocalendar()[1]

calc = int(week) % 2

if calc == 1:
	handler = makara.numerator[day-1]
	for i in range(0,len(makara.numerator[day-1])):
		list_of_lessons.append(handler[i])
elif calc == 0:
	handler = makara.denominator[day-1]
	for i in range(0,len(makara.denominator[day-1])):
		list_of_lessons.append(handler[i])

total_info["Fraction"] = fraction[calc]
total_info["Count_of_week"] = week
total_info["Weekday"] = weekdays[day]
total_info["lessons"] = list_of_lessons

print(total_info)

