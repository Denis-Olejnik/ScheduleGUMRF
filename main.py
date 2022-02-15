import datetime
import MakaraTest


weekdays = {1:"Понедельник",2:"Вторник",3:"Среда",4:"Четверг",5:"Пятница",6:"Суббота",7:"Воскресенье"}
deno_nume = {0:"Числитель",1:"Знаменатель"}

final_dict = {}
final_list = []

reader = datetime.datetime.today().isocalendar()[2]
week = datetime.datetime.today().isocalendar()[1]

final = int(week) % 2

c = 1

if int(reader) == 1:
	handler = MakaraTest.numerator[reader-1]
	for i in range(0,len(MakaraTest.numerator[reader])):
		final_list.append(handler[i])
else:
	handler = MakaraTest.denominator[reader-1]
	for i in range(0,len(MakaraTest.denominator[reader])):
		final_list.append(handler[i])

final_dict["Fraction"] = deno_nume[final]
final_dict["Count_of_week"] = week
final_dict["Weekday"] = weekdays[reader]
final_dict["lessons"] = final_list

print(final_dict)